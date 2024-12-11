# Mathematical Modelling - Fall 2024

## Assignment: Cutting Stock Problem
<!-- Describe cutting stock problem -->
Cuttin Stock Problem is a combinatorial optimization problem that arises in many industrial applications. The problem consists of cutting stocks of material into smaller pieces in order to meet the demand for smaller pieces. The objective is to minimize the number of stocks used to meet the demand for smaller pieces. The problem is NP-hard and can be solved using integer programming techniques.

Below is a demonstration of greedy algorithm for cutting stock problem.
<!-- Show gif file named demo/greedy.gif -->
![Greedy Algorithm](demo/greedy.gif)

## Installation
<!-- Describe how to install the project -->
To install the project, you need to have Python installed on your machine. You can install Python from the official website. Once you have Python installed, you can clone the repository and run the following command to install the required packages:
```bash
pip install -r requirements.txt
```

## Usage
<!-- Describe how to use the project -->
To use the project, you need to run the following command:
```bash
python main.py
```

## My policy
<!-- Describe my policy -->
The policy used in this implementation is a modified version of **Best Fit Decreasing (BFD)**. The steps of the policy are as follows:
1. **Sort Products**: The products are sorted by their **size (area)** in descending order.
2. **Best Fit for Stock**: For each product, we loop through the available stocks to find the one with the **smallest remaining space** that can fit the product.
3. **Place Product**: Once the best-fitting stock is found, the product is placed at the **first available position** that does not overlap with other products.
4. **Return Action**: The action is returned as the **stock index**, the **product size**, and the **position** where the product is placed in the stock.


## Contributing
<!-- Describe how to contribute to the project -->
To contribute to the project, you need to fork the repository and create a new branch. Once you have made your changes, you can create a pull request to merge your changes into the main branch.

## License
<!-- Describe the license under which the project is distributed -->
This project is distributed under the MIT License. See `LICENSE` for more information.