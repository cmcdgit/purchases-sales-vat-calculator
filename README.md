
● Contents
● UX (User Experience): User Stories, User Goals
● Design: Colorama, ASCII Art, Flowchart of Logic/Functions, User Feedback
● Application Features: Python Logic, Data/APIs used (optional)
● Future Features
● Technologies Used: Languages, Libraries, Programs
● Deployment: Step by step process for deploying to Heroku, API setup (optional)
● Testing: Validation of Python, Bugs, Input testing, User Stories, (Optional: Automated Testing)
● Credits: Content References, External resources, Acknowledgements

<!--  -->

![LTC logo](assets/images/python.png)



# VAT-Calculator-App 

## Intro

VAT-Calculator-App is a program designed for small businesses to use at Point-of-Sale/Purchase.  By taking the small amount of time required to log each 
transaction at the point of sale or purchase, and taking care to enter the correct details and assign the correct VAT rate, the application will allow any business self assessing for tax to track VAT owed or due on a monthly or year-to-date/annual basis, and will essentially 'do the book-keeping' for that small 
business.  I had the idea for this particular project after a discussion I had with a local small-business owner, and tried to solve for the very issue that 
they found themselves facing.  This application is currently in an MVP state and ideally would have a better front end for a better user experience.


## Features

### Existing Features

- **Main Menu**

  - The main menu is the landing page that a user will first interact with, it is currently quite basic hiding the real functionality that lies within the
  sub-menus for Purchases and Sales, and only allows a user decide whether they wish to interact with Purchases, Sales or when finished with the application,
  Exit. 

    <img src="assets/images/main-menu.png" alt="main menu" width="1200"/>

- **Sales/Purchases Menu**

  - The Sales/Purchases menus have 7 options to choose from
    1) Add a new transaction
        - It is assumed that a user will be using this at point-of-transaction so when a user selects to add
        a new transaction, in the background the code will determine the current month, and then check if 
        there is a sheet available for the current month.  If there is no sheet available yet for the
        current month a user will be prompted for input to decide if they would like to generate a 
        sheet for that month, and if/when the user agrees they will be prompted for the 3 pieces of information
        required to update either sheet: Details (name), Total (including VAT), and the VAT rate.

    2) Display all transactions for the current month
        - This option allows a user to view all transactions to date for the current month in the terminal.

    3) Display all transactions for the given month
        - This option allows a user to views all transactions for user determined month, if the user wishes to view 
        alternative months. The user will be presented with a list of the available months, which equates to available 
        monthly sheets, and they must choose from this list.

    4) Create a sales sheet for the current month
        - By selecting to create a s
    5) Show details on local VAT rates
    6) Display 'Totals' menu
    7) Return to the main menu 

    <img src="assets/images/sales-menu.png" alt="sales-menu" width="1200"/>

- **Recommended Books Page**

  - This page loads without content and waits for a user to select a programming language. When a selection is made 10 books display on the screen in various formations on the screen using flexbox. Each book has a blurb appearing over a background image of the book's cover with information on the book such as author, title, description, target reader and each book also has an active link that will navigate the user to that particular book on Amazon.

    <img src="assets/images/recommended-books.png" alt="recommended books screen" width="1200"/>

- **Footer**

  - The footer allows users to navigate to various "learn to code" social media sites, such as a Facebook page, an Instagram page, Twitter/X and also a Snapchat page.

    <img src="assets/images/ltc-social-links.png" alt="social media footer links" width="1200"/>

#### Button/Links

All buttons and links from within the Footer navigate the user to a newly opened tab featuring the relevent content. All Amazon links on the recommended books page navigate the user to the corresponding book on Amazon, again on a new tab.

### Features Left to Implement

There are a few things on the site that I would like to implement next:

- The blurb overlaying the book images on the book recommendations page would ideally only display while a user hovers over the image of the book's cover so that the focus is solely on the book the user is interested in.
- Other programming languages could be added to the site quite easily, and that would be something that I would like to do next.
- Social media sites are currently not active as the site does not yet have social media.
- Scores are tracked while a user is playing a game currently but this information is lost once a player restarts another game. Ideally this information would be captured and displayed in a leaderboard. By making it more competetive this should increase engagement in the site.
- Ideally there would be more questions available at all difficulty levels so that a user could opt to play a game at each of the available levels only.

## Manual Testing

- The site was tested extensively using Chrome devtools to confirm that all pages look and behave as expected across all device sizes.
- All links in the footer and also the Amazon links were tested to confirm that each will open a new browser tab and bring the user to the intended destination site.

### Validator Testing

- **Flake8**
  - No errors were found using the official W3C validator
- **Pylint**
  - No errors were found using the the official (Jigsaw) validator

## Deployment

- The site was deployed to GitHub pages. The steps to deploy are as follows:
  - In the GitHub repository, navigate to the Settings tab
  - From the source section drop-down menu, select the Master Branch
  - Once the master branch has been selected, the page will be automatically refreshed with a detailed ribbon display to indicate the successful deployment.

The live link can be found here - https://cmcdgit.github.io/learn-to-code/index.html

## Credits

### Content

- The icons in the footer were taken from [Font Awesome](https://fontawesome.com/)
- The questions for the Quiz page were generated using [ChatGPT](https://chatgpt.com/) and then successfully passed a test for plagiarism
- The array of books used to populate the book recommendations page were generated using [ChatGPT](https://chatgpt.com/) and also successfully passed a test for plagiarism
- The favicon icon in the tab/title bar was created by Soetarman Atmodjo and was taken from [The Noun Project](https://thenounproject.com/browse/icons/term/coding/)

### Media

- All book images are from (https://www.amazon.co.uk/)
- The background photo on the coding challenge page is available thanks to Karthik Swarnkar on [Unsplash](https://unsplash.com/photos/a-close-up-of-a-computer-screen-with-a-bunch-of-text-on-it-AoNvwL-Dmtw)
- The background photo on the recommended books page is available thanks to Radek Grzybowski on [Unsplash](https://unsplash.com/photos/macbook-pro-on-brown-wooden-table-inside-room-eBRTYyjwpRY)



<!--  -->

![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **May 14, 2024**

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!
