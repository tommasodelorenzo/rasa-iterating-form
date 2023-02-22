# Iterating forms in Rasa Open Source

Forms in [Rasa Open Source](https://rasa.com/docs/rasa/) are a great tool for a chatbot to gather a set of required information. While developing a chatbot myself, I needed to gather the same set of information `N` times, where `N` is chosen by the user. The best way of doing that would be to activate a form `N` consecutive times. I faced some problems trying to do that, so I hope this repo will save you some time.

The repo provides a complete, though minimal example on how to use `Rules` and `Custom Actions` to be able to iterate over a form N times.

The example resulting chatbot asks for the number `N` of iterations, and subsequently starts `N` times the form `my_form` consisting of a single required slot `lorem-ipsum`. At the end of every iteration, the filled slots are saved into the `iterations` slot for subsequent use.

Consider for instance you have a chatbot to book spots for a conference. The user can book up to 5 spots and the chatbot need to gather name and age of all the participants. In this case, `my_form` would have `name` and `age` required slots.


## How to use it
### Using virtual environment

1. Please follow [the official Rasa docs](https://rasa.com/docs/rasa/installation/environment-set-up) to create a virtual environment and install Rasa
2. Let the `action_endpoint` in `app/endpoints.yml` point to `localhost:5055`:
   ```
    action_endpoint:
    url: "http://localhost:5055/webhook"

    # action_endpoint:
    # url: "http://rasa_action_server:5055/webhook"
    ```
3. `cd app`
4. Train the model: `rasa train --domain domain`
5. Run the [action server](https://rasa.com/docs/action-server/running-action-server/): `rasa run actions`
6. In a new shell in the `app` folder, activate the environment and run Rasa shell: `rasa shell` and interact with the chatbot

### Using docker compose
As of February 2023, the Rasa Docker image is not compatible with `M1/M2` powered Mac.
1. Let the `action_endpoint` in `app/endpoints.yml` point to the `rasa_action_server` service:
   ```
    # action_endpoint:
    # url: "http://localhost:5055/webhook"

    action_endpoint:
    url: "http://rasa_action_server:5055/webhook"
    ```
2. `cd docker`
3. Build the images: `docker compose build`
4. Run the services: `docker compose up -d`
5. Train the model: `docker compose run --rm rasa_core train --domain domain`
6. Run Rasa shell `docker compose run --rm rasa_core shell --domain domain` and interact with the chatbot

The `docker/docker-compose.yml` comes with the possibility of setting up a custom tracker store using `postgreSQL`, but it is commented by default. If you want to unlock it, you must also uncomment the `tracker_store` related lines in `app/endpoints.yml`:
````
tracker_store:
    type: SQL
    dialect: "postgresql" 
    url: "rasa_tracker_store" 
    db: "rasa" 
    username: "rasa"
    password: "rasa"
````
   


