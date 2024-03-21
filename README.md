# BudgetApp Django Project

Welcome to the BudgetApp Django Project! This project is designed to help users manage their finances by providing features for user authentication, expense tracking, earnings tracking, and financial status visualization through a dashboard.

## Apps:

### Accounts
- **UserProfile:** View and manage user profiles.
- **User Authentication:** Authenticate users.

### MoneyManagement
- **Expense Tracking:** Add and view daily expenses.
- **Earnings Tracking:** Add and view monthly earnings.
- **Financial Status / day:** Manage different categories to store the amount of money.

### DataVisualisation - Dashboard
- **Dashboard:** Display total earnings, total expenses, and their month-to-month comparisons.
- **Bar Chart:** Utilizes django-chartjs to present data with bar charts for expenses and the amount of money you have.

## Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Run the development server: `python manage.py runserver`
4. Create user 

## Contributing
Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request.
