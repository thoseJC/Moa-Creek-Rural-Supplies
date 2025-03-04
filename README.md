![mcrs ERDs](static/images/mcrs14.png "mcrs ERDs")
# Local developement #
### step 1: Create virtual development on local ###
Follow this Tutorio : https://code.visualstudio.com/docs/python/tutorial-flask 

### step 2: Install project dependencies ###
after create virtual enviroment susefully
run command :
` pip install -r requirements.txt `

### step 3: Create databse connect file ###
1. create a file name `connect.py` in the same folder as ` app.py `
2. add belows information into `connect.py ` file:
   
```
    dbuser = "root" # Your MySQL username - likely 'root'
    dbpass = "password" # ---- PUT YOUR PASSWORD HERE ----
    dbhost = "localhost" 
    dbport = "3306"
    dbname = "MRCDB"
```


## Moa Creek Rural Supplies Website and System Upgrade
### Project Overview
Moa Creek Rural Supplies is an online retailer based in Alexandra, Central Otago. We are excited to announce an upgrade to our existing website along with the implementation of a new order and inventory management system. This initiative is designed to modernize our platform, enhancing the way we showcase and manage a diverse range of agricultural products from animal health to machinery and oils. Our goal is to provide a user-friendly interface that boosts product promotion and elevates customer service levels.

### Key Features
* User-Friendly Homepage: Redesigned for easier navigation and enhanced product display.
* Advanced Order and Inventory Management: Efficient management of stock with real-time updates.
* Enhanced Payment Processes: Integration of multiple payment methods ensuring secure transactions.
* Comprehensive Reporting Tools: Provide valuable insights into sales trends and customer behaviors.
* Customer Engagement Tools: A points-based loyalty program and sophisticated account management features.
### Technical Specifications
* Frontend Development
Technologies: HTML, CSS, Bootstrap
Features: Responsive design that adapts to device screens ensuring optimal user experience.
* Backend Development
Technologies: Python, Flask
Features: Server-side logic and dynamic content generation.
* Database Management
Technology: SQL
Features: Robust data handling and complex query execution.
### System Roles
* Customer Interface: Enables customers to browse products, manage their accounts, and receive updates on their orders.
* Staff Functionality: Facilitates product, order, and customer interaction management.
* Manager Functionality: Can execute all the staff tasks, manage promotions, accounts of all roles management, and reports management.
* Administrative Access: Provides tools for operational oversight and system customization.
  
![image](https://github.com/user-attachments/assets/bb98ed57-f7bb-4fc2-9158-ec0ace54fa3f)
![image](https://github.com/user-attachments/assets/92c0b2c4-1046-4127-b394-e1d09261399f)
![image](https://github.com/user-attachments/assets/b3d670cc-6db5-427b-9cf9-a05530761fa1)


