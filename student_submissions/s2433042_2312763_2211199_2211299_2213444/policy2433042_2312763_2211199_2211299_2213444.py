from queue import PriorityQueue
from policy import Policy
import numpy as np


class Policy2433042_2312763_2211199_2211299_2213444(Policy):
    def __init__(self, policy_id=1):
        """
        Khởi tạo policy.
        :param policy_id: 1 - BFD, 2 - B&B
        """
        assert policy_id in [1, 2], "Policy ID must be 1 or 2"
        self.policy_id = policy_id

    def get_action(self, observation, info):
        """
        Chọn hành động dựa trên policy_id.
        """
        if self.policy_id == 1:
            # Giải thuật BFD
            return self._get_action_bfd(observation, info)
        elif self.policy_id == 2:
            # Giải thuật B&B
            return self._get_action_bb(observation, info)

    # ==================== BFD Implementation ====================
    def _get_action_bfd(self, observation, info):
        """
        Triển khai giải thuật BFD.
        """
        # Lấy danh sách sản phẩm và sắp xếp theo diện tích giảm dần
        products = sorted(
            [p for p in observation["products"] if p["quantity"] > 0],
            key=lambda x: x["size"][0] * x["size"][1],
            reverse=True,
        )

        for product in products:
            prod_size = product["size"]
            best_stock_idx = -1
            best_position = None
            min_waste = float("inf")

            # Duyệt qua tất cả các stock
            for stock_idx, stock in enumerate(observation["stocks"]):
                stock_w, stock_h = self._get_stock_size_(stock)

                # Kiểm tra khả năng đặt sản phẩm
                for x in range(stock_w - prod_size[0] + 1):
                    for y in range(stock_h - prod_size[1] + 1):
                        if self._can_place_(stock, (x, y), prod_size):
                            # ENV tự kiểm tra xoay, không cần xử lý thủ công
                            waste = self._calculate_waste(stock, (x, y), prod_size)
                            if waste < min_waste:
                                best_stock_idx = stock_idx
                                best_position = (x, y)
                                min_waste = waste

            # Nếu tìm thấy vị trí phù hợp, trả về hành động
            if best_stock_idx != -1 and best_position is not None:
                return {"stock_idx": best_stock_idx, "size": prod_size, "position": best_position}

        # Nếu không tìm thấy, trả về hành động mặc định
        return {"stock_idx": -1, "size": [0, 0], "position": (0, 0)}

    # ==================== B&B Implementation ====================
    def _get_action_bb(self, observation, info):
        """
        Triển khai giải thuật B&B.
        """
        # Lấy danh sách sản phẩm và stock
        products = [
            {"size": p["size"], "quantity": p["quantity"]}
            for p in observation["products"]
            if p["quantity"] > 0
        ]
        stocks = observation["stocks"]

        # Hàng đợi ưu tiên cho B&B
        queue = PriorityQueue()
        queue.put((0, {"stocks": stocks, "products": products, "actions": []}))

        best_solution = None
        min_trim_loss = float("inf")

        # Vòng lặp chính của B&B
        while not queue.empty():
            _, state = queue.get()

            # Kiểm tra điều kiện kết thúc
            if all(p["quantity"] == 0 for p in state["products"]):
                trim_loss = self._calculate_trim_loss(state["stocks"])
                if trim_loss < min_trim_loss:
                    min_trim_loss = trim_loss
                    best_solution = state["actions"]
                continue

            # Tạo nhánh mới
            for product_idx, product in enumerate(state["products"]):
                if product["quantity"] == 0:
                    continue

                for stock_idx, stock in enumerate(state["stocks"]):
                    stock_w, stock_h = self._get_stock_size_(stock)

                    for x in range(stock_w - product["size"][0] + 1):
                        for y in range(stock_h - product["size"][1] + 1):
                            if self._can_place_(stock, (x, y), product["size"]):
                                # Tạo trạng thái mới
                                new_state = self._branch_state(
                                    state, stock_idx, product_idx, (x, y), product["size"]
                                )
                                # Tính toán giá trị bound
                                bound = self._calculate_bound(new_state)
                                queue.put((bound, new_state))

        # Trả về hành động từ nhánh tốt nhất
        if best_solution:
            return best_solution[0]  # Trả về hành động đầu tiên

        # Nếu không tìm thấy, trả về hành động mặc định
        return {"stock_idx": -1, "size": [0, 0], "position": (0, 0)}

    # ==================== Helper Methods ====================
    def _calculate_waste(self, stock, position, prod_size):
        """
        Tính toán lãng phí khi đặt sản phẩm vào stock
        """
        pos_x, pos_y = position
        prod_w, prod_h = prod_size

        used_cells = np.count_nonzero(stock[pos_x : pos_x + prod_w, pos_y : pos_y + prod_h] != -2)

        return used_cells - (prod_w * prod_h)

    def _branch_state(self, state, stock_idx, product_idx, position, size):
        """
        Tạo nhánh mới từ trạng thái hiện tại
        """
        new_stocks = [np.copy(stock) for stock in state["stocks"]]
        new_products = [p.copy() for p in state["products"]]

        pos_x, pos_y = position
        new_stocks[stock_idx][
            pos_x : pos_x + size[0], pos_y : pos_y + size[1]
        ] = product_idx
        new_products[product_idx]["quantity"] -= 1

        new_actions = state["actions"] + [
            {"stock_idx": stock_idx, "size": size, "position": position}
        ]

        return {"stocks": new_stocks, "products": new_products, "actions": new_actions}

    def _calculate_trim_loss(self, stocks):
        """
        Tính toán mức độ lãng phí
        """
        trim_loss = 0
        for stock in stocks:
            trim_loss += (stock == -1).sum()
        return trim_loss

    def _calculate_bound(self, state):
        """
        Tính toán giá trị bound
        """
        remaining_products = sum(p["quantity"] for p in state["products"])
        remaining_space = sum((stock == -1).sum() for stock in state["stocks"])
        return remaining_products / max(remaining_space, 1)