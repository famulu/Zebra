# Zebra: A minimalist spreadsheet website

### Video Demo: https://youtu.be/AOuuqwAy3XQ

### Description: A spreadsheet with the minimum amount of necessary features.
For most use cases, we don't need the overwhelming number of features offered by conventional programs.
Instead of being more useful, it's more likely to make the user less productive by giving them decision fatigue
and the feeling of missing out or that there is a better way
to do what they're doing. This spreadsheet incorporates only the absolute essential features, all in the way of
easy to use buttons at the top of the website. Simple, minimalist and practical. In arrowkeys.js, I implemented a function that
allows the user to navigate between different cells using keyboard input.
Enter and down arrow key to go the cell below.
Tab and right arrow key to go the cell to the right of the current cell.
Up arrow key to go to the cell above the current cell.
Left arrow key to go to the cell to the left of the current cell.
The logo of the website (a picture of a zebra) was taken from a logo website.
Credit: https://icons8.com/icon/8864fJDRaHhN/zebra

### Features include:

#### Save
A way to store all the data and which cells they are in using a sqlite database. Your data won't be lost
even if you log out as long as you remember to save before you do.

#### Export
Allows you to export your spreadsheet to your device as a csv file. Do you need to access features on a
different spreadsheet program or share the csv file with someone. Use the export button and
have it download to your local device.

#### Import
Local .csv files can be imported to the website and saved to the database. Do you have a csv file, but
you don't want to manually input all its contents to the spreadsheet. No problem, just import it, the program
will automatically input them into the spreadsheet for you.

#### Insert
Insert new rows/columns to the spreadsheet. Don't have enough rows or columns? Just insert new ones at the end
of your spreadsheet. Up to a limit of 1000 rows and columns.

#### Change Password
Change current password to new password. Note: you will be automatically logged out when you do so. Don't think
your password is secure enough? Change it easily by just using your current password.

#### Log Out
Once done with all work, just log out, but don't forget to press save if you want to see
your progress the next time you log in

#### Register
Register for an account and start spreadsheeting. You can select the number of rows and columns you want in your spreadsheet and if
you don't select anything, the program will default to 26 columns (number of letters in the english alphabet) and 100 rows (0 to 99)

#### Additional features
You will be prompted with a welcome alert every time you log in. (In the form, "Welcome, {username}")