### The startup
- make a .env file with the connections to the  database
- create a sqlalchemy ORM class for the corresponding table in the database with all the connections etc in one file
- select from the db the rows (object), which meet some arbitrary filter criteria
- map these objects to the rows of a table widget and fill the table widget with the attributes of the objects
- move the pointer to the next row
    - if the actions on selecting some cell from the table was implemented, make sure on this first selection no db commit happens
- open the url of the very first object in the table widget in the browser

### Selecting a cell
- whenever I choose a next cell using either a button, mouseclick or hotkey
    - if it is a new row, which i can check by the row id, if it is the same as the previous one
        - if the previous None
            - commit nothing
            - open the url in the browser
        - if the previous != new
            - commit changes on the previous row
                - take the row cell text and do Obj(**attrs)
            - open a url in the browser
        - if the new is None (which probably means deselected)
            - commit previus
            - do not update the previous cell to None

- on every commit reflect the change by appending the change in a log

### Refresh
- simply take new objects and populate the table widget with it and do the Start up procedure
- do not forget to ignore the row change - i can provide a boolean which says the refresh is taking place

### Log operations
- add an item to the task bar for log
    - read - pop up window, where i can see the log content
    - purge - will simply blank out the log file - can be also a pop up window signaling this was done

### ideas
- multiple tabs, one of them is the circle tool. addresses + radius  -> gps -> i can open on a new tab the tool for circles


        