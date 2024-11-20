**Project Title**: 
    Personal Finance Manager

**Project Description**:
    The Personal Finance Manager is a desktop application designed to help users track their personal expenses and manage category-based budgets. It provides an intuitive graphical interface for adding and categorizing expenses, monitoring spending, setting budget limits and visualizing spending patterns with charts. Users can easily manage their financial data and make informed decisions based on their current spending trends.

**Features**:
    Expense Tracking:
        Record expenses with details such as date, amount, category and description.
    Category-based Budgets: 
        Set budget limits for different categories (for example: food, entertainment) and receive warnings if you exceed them.
    Spending Analysis: 
        Calculate and display the total spending and spending by category.
    Spending Visualization: 
        View spending distribution through pie charts.
    Data Persistence: 
        Expenses and budgets are saved in JSON format for easy access and storage.
    User-friendly GUI:
        Simple, scrollable and maximized window layout for ease of navigation.
    Clear Data:
        Options to clear expenses, budgets or all data with confirmation prompts.

**Installation**: 
    1. Clone the repository:
            git clone <repository-url>
            cd personal-finance-manager
    2. Install required dependencies: 
        Install the required Python libraries using the pip command:
            pip install matplotlib tk
    3. Run the application:
            python personal_finance_manager.py

**Usage:**
    Adding an Expense:
        Enter the Date (in DD-MM-YYYY format).
        Input the Amount (e.g., 50.75).
        Specify the Category (e.g., "Food", "Entertainment").
        Optionally, add a Description for the expense.
        Click "Add Expense" to save the expense.

    Setting a Budget:
        Enter the Category (e.g., "Food").
        Enter the Budget Amount (e.g., 200).
        Click "Update Budget" to save the budget for that category.

    Viewing Total Spending:
        Click the "Show Total Spending" button to see the cumulative amount spent across all categories.

    Viewing Spending by Category:
        Click the "Show Spending by Category" button to view the total spending per category.

    Viewing Spending Distribution:
        Click the "Show Spending Distribution" button to visualize the spending distribution as a pie chart.

**Configuration:**
    The program does not require additional configuration files. All data (expenses and budgets) is automatically stored in JSON files (expenses.json and budgets.json) in the working directory.

**Examples:** 
    Example: Adding an Expense
            Date: 25-10-2024
            Amount: 50.75
            Category: Food
            Description: Lunch at a restaurant
        After filling in the fields, click "Add Expense".

    Example: Setting a Budget 
            Category: Entertainment
            Budget: 150
        After entering the category and budget, click "Update Budget".

    Example: Visualizing Spending Distribution
        After recording multiple expenses across categories, click "Show Spending Distribution" to view the distribution in a pie chart.

**Troubleshooting:** 
    Invalid Date: Ensure the date format is in DD-MM-YYYY.
    Invalid Amount: Ensure the amount is a valid numerical value (e.g., 50.75).
    Budget Exceeded: If an expense exceeds the set budget, a warning will prompt you to confirm the action.
    Missing Libraries: Ensure you have installed all required libraries (matplotlib and tkinter).

**Credits:** 
    Tkinter: Used for creating the graphical user interface.
    Matplotlib: Used for generating pie charts to visualize spending patterns.
    Creator: Parisa Singh. 

**License:** 
    This project is licensed under the MIT License. 
    [LICENSE](https://opensource.org/license/mit) 