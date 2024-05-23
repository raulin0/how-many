## How Many: Easy-to-use tool to build decks with a more consistent mana base

Magic: The Gathering Decklist Analyzer is a tool designed to analyze and process decklists for the popular trading card game Magic: The Gathering. It allows users to input a decklist and provides insights into the composition of the deck, including card types, mana costs, and more. This project was developed with the aim of providing a comprehensive analysis tool for Magic: The Gathering players and enthusiasts.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Practical Example School Manager API](#practical-example-school-manager-api)
  - [Running the Container](#running-the-container)
- [Authentication](#authentication)
- [Usage](#usage)
  - [Accessing Swagger UI](#accessing-swagger-ui)
  - [Accessing ReDoc](#accessing-redoc)
- [Endpoints](#endpoints)
  - [Cards](#cards)
  - [Decks](#decks)
  - [CardDecks](#carddecks)
- [Examples](#examples)
- [Filters](#filters)
- [Contributing](#contributing)

## Getting Started

### Prerequisites

- Python 3.11+
- Django
- PostgreSQL
- Docker

### Running the Container

1. Clone this repository to your local machine:

    ```shell
    git clone https://github.com/how-many.git
    ```

2. Change into the project directory:

    ```shell
    cd path/to/how-many
    ```

3. Set enviroment variables:

    Add an .env file to set the enviroment variables.

    3.1. Set DJANGO_ENV:

    - Set the value of the DJANGO_ENV variable to "development" or "production", depending on which environment you are working in:

        ```
        DJANGO_ENV=replace_this_to_development_or_production
        ```
    
    3.2. Set SECRET_KEY:

    - Access the Python Interactive Shell and import the get_random_secret_key() function from django.core.management.utils:

        ```shell
        >>> from django.core.management.utils import get_random_secret_key
        ```

    - Generate the Secret Key in the Terminal using the get_random_secret_key() function:

        ```shell
        >>> print(get_random_secret_key())
        ```

    - Set django's SECRET_KEY:

        ```
        SECRET_KEY=replace_this_with_your_generated_secret_key
        ```
        
    3.3. Set the database variables:

    - By default, django uses the sqlite3 database, but it can be changed to another, such as PostgreSQL, which we will be using in this project. To do this, you need to set the environment variables for the database configuration
    
        ```
        PG_NAME=replace_this_with_your_database_name
        PG_USER=replace_this_with_your_database_user
        PG_PASSWORD=replace_this_with_your_database_password
        PG_HOST=replace_this_with_your_database_host
        PG_PORT=replace_this_with_your_database_port
        ```
    
    Set the superuser variables:

    - Finally, you will need to set the DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD environment variables for the superuser settings, which will be used to create it.
    
        ```
        DJANGO_SUPERUSER_USERNAME=replace_this_with_your_username
        DJANGO_SUPERUSER_EMAIL=replace_this_with_your_email
        DJANGO_SUPERUSER_PASSWORD=replace_this_with_your_password
        ```

4. Run

    4.1. Locally:

    You can run the application detached from the terminal by adding the -d option. Inside the directory, run the following command in a terminal.

    ```shell
    docker compose up -d --build
    ```

    Open a browser and view the application at http://localhost:8000.

    In the terminal, run the following command to stop the application.

    ```shell
    docker compose down
    ```

    4.2. In production:

    Docker offers us a number of advantages for when we put a service into production, such as: portability, isolated environments, ease of deployment, etc. That's why we chose to use it.

    - Make sure you are logged in to Docker Hub:

        ```shell
        docker login
        ```
        This will ask for your Docker Hub credentials.

    - Build the Docker image:

        ```shell
        docker build -t your-user/your-repository:tag .
        ```
        - your-user: Your username on Docker Hub.
        - your-repository: Name of the repository you want to create.
        - tag: Version or tag of your image.

    - Upload the image to Docker Hub:

        ```shell
        docker push your-user/your-repository:tag
        ```

        This will send your image to Docker Hub, making it available for use.

## Authentication

The API uses Basic Authentication to secure endpoints, except for the DeckModelViewSet action responsible for processing the data of a decklist. To access protected endpoints, you will need to include your credentials in the request headers. Make sure to use HTTPS in production for secure authentication.

## Usage

### Accessing Swagger UI

Swagger UI provides an interactive interface for exploring and testing the API endpoints. To access Swagger UI, open your web browser and go to:

-   ```http
    http://localhost:8000/swagger/
    ```
    if the API is running locally.

### Accessing ReDoc

ReDoc is another documentation tool that provides a clean and responsive way to browse API documentation. To access ReDoc, open your web browser and go to:

-   ```http
    http://localhost:8000/redoc/
    ```
    if the API is running locally.

ReDoc presents the API documentation in a visually appealing format, making it easy to understand and navigate.

## Endpoints

### Cards

- **GET /cards/**:
    - **Description**: Retrieve a list of all cards.
    - **Response**: A JSON array of card objects.
- **GET /cards/{card_id}/**:
    - **Description**: Retrieve details of a specific card by its ID.
    - **Response**: A JSON object containing the details of the card.
- **POST /cards/**:
    - **Description**: Create a new card record
    - **Request Body**: JSON object containing card details (e.g., name, layout, mana cost, etc.).
    - **Response**: The created card object with its new ID.
- **PUT /cards/{card_id}/**:
    - **Description**: Update the details of a specific card.
    - **Request Body**: JSON object with updated card details.
    - **Response**: The updated card object.
- **DELETE /cards/{card_id}/**:
    - **Description**: Delete a card record by its ID.
    - **Response**: Confirmation of deletion.
- **GET /cards/{card_id}/decks/**:
    - **Description**: Retrieve a list of decks that contain a specific card.
    - **Response**: A JSON array of deck objects associated with the card.

### Decks

- **GET /decks/**:
    - **Description**: Retrieve a list of all decks.
    - **Response**: A JSON array of deck objects.
- **GET /decks/{deck_id}/**:
    - **Description**: Retrieve details of a specific deck by its ID.
    - **Response**: A JSON object containing the details of the deck.
- **POST /decks/**:
    - **Description**: Create a new deck.
    - **Request Body**: JSON object containing deck details (e.g., is_commander_deck, has_companion, etc.).
    - **Response**: The created deck object with its new ID.
- **PUT /decks/{deck_id}/**:
    - **Description**: Update the details of a specific deck.
    - **Request Body**: JSON object with updated deck details.
    - **Response**: The updated deck object.
- **DELETE /decks/{deck_id}/**:
    - **Description**: Delete a deck by its ID.
    - **Response**: Confirmation of deletion.
- **POST /decks/process/**:
    - **Description**: Process and save a decklist from provided text.
    - **Request Body**: JSON object containing the decklist text.
    - **Response**: The processed and saved deck object.
- **GET /decks/{deck_id}/cards/**:
    - **Description**: Retrieve a list of cards within a specific deck.
    - **Response**: A JSON array of card objects associated with the deck.

### CardDecks

- **GET /card-decks/**:
    - **Description**: Retrieve a list of all card-deck associations.
    - **Response**: A JSON array of card-deck objects.
- **GET /card-decks/{card_deck_id}/**:
    - **Description**: Retrieve details of a specific card-deck association by its ID.
    - **Response**: A JSON object containing the details of the card-deck association.
- **POST /card-decks/**:
    - **Description**: Create a new card-deck association.
    - **Request Body**: JSON object containing card-deck details (e.g., card_id, deck_id, section, quantity, etc.).
    - **Response**: The created card-deck object with its new ID.
- **PUT /card-decks/{card_deck_id}/**:
    - **Description**: Update the details of a specific card-deck association.
    - **Request Body**: JSON object with updated card-deck details.
    - **Response**: The updated card-deck object.
- **DELETE /card-decks/{card_deck_id}/**:
    - **Description**: Delete a card-deck association by its ID.
    - **Response**: Confirmation of deletion.

## Examples

Here are some examples of using the API:

- **Create a new card**:

    ```http
    POST /cards/
    Content-Type: application/json

    {
        "name": "Lightning Bolt",
        "layout": "normal",
        "mana_cost": "{R}",
        "cmc": 1,
        "type_line": "Instant",
        "rarity": "common",
        "oracle_text": "Lightning Bolt deals 3 damage to any target.",
        "is_land": false,
        "is_cheap_card_draw_spell": false,
        "is_cheap_mana_ramp_spell": false,
        "is_land_spell_mdfc": false
    }
    ```

- **Retrieve a list of decks**:

    ```http
    GET /decks/
    ```

- **Update a deck**:

    ```http
    PUT /decks/1/
    Content-Type: application/json

    {
        "is_commander_deck": true,
        "has_companion": false,
        "maindeck_card_count": 100,
        "non_land_card_count": 60,
        "non_land_cmcs_count": 40,
        "cheap_card_draw_spell_count": 10,
        "cheap_mana_ramp_spell_count": 5,
        "non_mythic_land_spell_mdfc_count": 2,
        "mythic_land_spell_mdfc_count": 1,
        "average_cmc": 2.5,
        "recommended_number_of_lands": 38
    }
    ```

- **Delete a card**:
    ```http
    DELETE /cards/1/
    ```

- **Process a decklist**:
    ```http
    POST /decks/process/
    Content-Type: application/json

    {
        "decklist_text": "Decklist text here"
    }
    ```
    
## Filters

You can filter the results of GET requests using the following query parameters for each endpoint:

- **/cards/?<filter>**:
    - **name**: Filter by card name (contains).
    - **layout**: Filter by card layout (exact).
    - **mana_cost**: Filter by card mana cost (exact or contains).
    - **cmc**: Filter by converted mana cost (exact, greater than or equal, less than or equal).
    - **type_line**: Filter by type line (contains).
    - **rarity**: Filter by rarity (exact).
    - **oracle_text**: Filter by oracle text (contains).
    - **is_land**: Filter by whether the card is a land.
    - **is_cheap_card_draw_spell**: Filter by whether the card is a cheap card draw spell.
    - **is_cheap_mana_ramp_spell**: Filter by whether the card is a cheap mana ramp spell.
    - **is_land_spell_mdfc**: Filter by whether the card is a land spell MDFC.

- **/decks/?<filter>**:
    - **created_at_date**: Filter by creation date.
    - **created_at_datetime**: Filter by creation datetime.
    - **is_commander_deck**: Filter by whether the deck is a commander deck.
    - **has_companion**: Filter by whether the deck has a companion.
    - **maindeck_card_count**: Filter by the number of cards in the main deck.
    - **non_land_card_count**: Filter by the number of non-land cards.
    - **non_land_cmcs_count**: Filter by the number of non-land CMCs.
    - **heap_card_draw_spell_count**: Filter by the number of cheap card draw spells.
    - **cheap_mana_ramp_spell_count**: Filter by the number of cheap mana ramp spells.
    - **non_mythic_land_spell_mdfc_count**: Filter by the number of non-mythic land spell MDFCs.
    - **mythic_land_spell_mdfc_count**: Filter by the number of mythic land spell MDFCs.
    - **average_cmc**: Filter by the average converted mana cost.
    - **recommended_number_of_lands**: Filter by the recommended number of lands.

- **/card-decks/?<filter>**:
    - **card_name**: Filter by card name (contains).
    - **section**: Filter by section (exact).

## Contributing

### Tool

This project uses `Poetry` for environment management and library installation, so make sure you have Poetry installed for this contribution:

```sh
pipx install poetry
```

### Contributing Process

1. Fork the repository on GitHub.

2. Clone your forked repository to your local machine.

    ```
    git clone https://github.com/<your-user>/how-many.git
    ```

3. Install dependencies.

    ```
    poetry install
    ```

4. Use Git Flow as your workflow to help organize the versioning of your code.

    Git Flow works with two main branches, Develop and Master, which last forever; and three supporting branches, Feature, Release and Hotfix, which are temporary and last until you merge with the main branches.
    So instead of a single Master branch, this workflow uses two main branches to record the project's history. The Master branch stores the official release history, and the Develop branch serves as a merge branch for features.
    Ideally, all commits in the Master branch are marked with a version number.
    - **Master/Main Branch**: where we have all the production code. All new features that are being developed, at some point, will be merged or associated with the Master. The ways to interact with this branch are through a Hotfix or a new Release.
    - **Develop Branch**: where the code for the next deployment is located. It serves as a timeline with the latest developments, this means that it has features which have not yet been published and which will later be associated with the Master branch.
    - **Feature Branch**: used for the development of specific features. It is recommended that these branches follow a naming convention, the most used convention is to start the branch name with feature, for example, "feature/feature-name". It is important to know that these feature branches are always created from the Develop branch. Therefore, when they are finished, they are removed after performing the merge with the Develop branch. If we have ten features to develop, we create ten independent branches. It is important to note that feature branches cannot have interaction with the master branch, only with the develop branch.
    - **Hotfix Branch**: created from the master to make immediate fixes found in the production system. When completed, it is deleted after merge with the master and develop branches. We have a hotfix branch for every hotfix we need to implement! The big difference between Feature Branches and Hotfix Branches is that Hotfixes are created from the Master Branch and when we finish them, they are merged into both the Master Branch and the Develop Branch. This is because the bug is in both environments. Also, when we close a Branch Hotfix, we have to create a tag with the new project version. This is because every change we make in the Branch Master needs a tag that represents it.
    - **Release Branch**: serves as a bridge for merge from Develop to Master. It works as a testing environment and is removed after the merge tests with the Master. If a bug is found and changes are made, it must also be synchronized with the Develop Release. Finally, when we close a Branch Release, we have to create a tag with the new release version of the software, so that we can have a complete history of the development.

5. Make the necessary changes to the codebase.

6. In case of changes to the project dependencies, generate a new requirements.txt file that will be used in docker.

    ```sh
    pip freeze > requirements.txt
    ```

7. Commit your changes with a descriptive commit message using the conventional commit format.

	```sh
	<type>[optional scope]: <description>
	[optional body]
	[optional footer]
	```

8. Push your branch to your forked repository on GitHub. For an example of a feature:

	```bash
	git push origin <feature/feature-name>
	```

9. Open a pull request from your branch to the main repository.

10. Wait for the maintainers to review your changes and address any feedback if necessary.

11. Once your changes are approved, they will be merged into the main repository.

If you have any questions or need assistance during the contribution process, feel free to open an [issue on the project's GitHub repository](https://github.com/Raulin0/how-many/issues) and ask for help.