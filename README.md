# Notes API

Finished with creating a notes REST API. Instructions for running the app aswell as running tests is found in `instruction/README.md`. Test coverage of 95% has been achieved. Most of the tests was done by testing endpoints with mocked database that is recreated for every test group, so tests don't intervene with actual data. If you have any questions or concerns please feel free to contact me at krizovid@gmail.com

Disclaimer: Due to simplification for testing party I pushed both the environment and database file to Github. Normally I would provide template file for both and not actually push files to origin. But again for easier setup process and it not being actual production code I decided to just push the two files.

_________________________________________________________________________________________________________________________________________________________________________________

Create REST API that allows users to manage their notes.
Notes can be organized into folders for easier management.
API should allow user authentication through basic HTTP authentication (username and password).
The goal is to build a simple but secure and easily scalable service.

### Entities
* Basic user info (name, username, password) should be stored in the database
* Users own multiple folders that can be named
* Folders contain multiple notes that can be named
* Notes can be shared (visible to all users and unauthenticated viewers) or private (visible only to the creator)
* Notes can be of 2 different types
  * Text note - has text body
  * List note - has list items that contain text body

### API
* API for users is not needed, data can be seeded into the database
* Should support CRUD actions for folders
* Should support CRUD actions for notes
* Implement at least 2 out of 3
  * Pagination
  * Sorting
    * By note shared option (public/private)
    * By note heading
  * Filtering
    * By note folder
    * By note shared option (public/private)
    * By note text

### Directions
* You can use any programming language/framework for REST API
* All data should be saved in database of your choice
* No frontend is needed, only API
* Users are authenticated via username and password. Users authentication data (usernames/passwords) can be generated and seeded in the provided database since API for users is not required.

### Submission
* Fork this repository and commit the code there
  * Add [instructions](instructions/README.md)
  * Add [database seed](database/README.md)
  * Add [credentials](credentials/README.md)
