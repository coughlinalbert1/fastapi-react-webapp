### fastapi-warehouse
Virtual environment isn't necessary, but if you dont, you might run into conflicting libraries so I recommend it even tho its annoying asf lol.
If you wanna try without, just skip to the download the requirements step for both requirements.txt then skip to the running the servers and scripts. You'll still need
multiple terminals or two VSC windows with split terminals. You may have to change it to this without a venv.
```
python3 -m pip install -r requirements.txt --no-cache-dir
```
#### Create virtual environment
In the terminal, make sure the current working directory is something like ... fastapi-warehouse
```
python3 -m venv venv
```

#### Start the venv
```
source venv/bin/activate
```
You should see something like (venv) on the current line in the terminal.

#### Download the dependencies
```
pip install -r requirements.txt --no-cache-dir
```
You should see a bunch of stuff downloading lmao

#### Restart venv and run the uvicorn server
```
deactivate
```
Then start it up again
```
source venv/bin/activate
```
Then run the server with the reload flag
```
uvicorn main:app --reload
```
#### Run the script that allows communication
In a new terminal but still same directory, open the venv again.
```
source venv/bin/activate
```
Then run the script
```
python fulfillment.py
```

Here is what you should see if everything went right.
<img width="1709" alt="image" src="https://github.com/coughlinalbert1/fastapi-react-webapp/assets/111651444/fb585e42-f529-40a3-8ee4-585e64b7d793">

Now go to your browser and type [localhost:8000](http://localhost:8000/docs#/)
<img width="1709" alt="image" src="https://github.com/coughlinalbert1/fastapi-react-webapp/assets/111651444/edfc58a8-135b-49b9-8799-0d83a275f4f6">





### fastapi-store
Yes I do want to kms rn so you are not alone. But once youve done this all, you just have to open the venv and start the servers. Or put it in docker and push a single button. But I don't feel like messing with that for this example project lmao.

#### Create virtual environment
In the terminal, make sure the current working directory is something like ... fastapi-warehouse
```
python3 -m venv venv
```

#### Start the venv
```
source venv/bin/activate
```
You should see something like (venv) on the current line in the terminal.

#### Download the dependencies
```
pip install -r requirements.txt --no-cache-dir
```
You should see a bunch of stuff downloading lmao

#### Restart venv and run the uvicorn server
```
deactivate
```
Then start it up again
```
source venv/bin/activate
```
Then run the server with the reload flag and in a different port because the default for uvicorn is 8000 and that is occupied by the store microservice.
```
uvicorn main:app --port 8001 --reload
```
#### Run the script that allows communication
In a new terminal but still same directory, open the venv again.
```
source venv/bin/activate
```
Then run the script
```
python update.py
```

If everything went right, it should look similar to before.

<img width="1709" alt="image" src="https://github.com/coughlinalbert1/fastapi-react-webapp/assets/111651444/3d0d8738-4bc2-4ff3-920a-dd3f9c350a97">

Now go to browser and in a new tab [localhost:8000](http://localhost:8001/docs#/)


### Using the API
Ok so once everything is open like this
<img width="1709" alt="image" src="https://github.com/coughlinalbert1/fastapi-react-webapp/assets/111651444/b0718785-e637-47d7-8c4a-4b96e16b534f">
We can start using it.

#### Buying a product
<img width="1067" alt="image" src="https://github.com/coughlinalbert1/fastapi-react-webapp/assets/111651444/e5004cba-a09d-4bb6-97b1-ca5330837bf0">
So what is happening here is that we make a get request. This one goes into the redis db and gets all of the products that I created earlier using the Post request. In the code you can see that products do not have an id specified in the models. Redis creates pks for each entry automatically. We will need this. So lets copy one of the product ids. I'll do the first one 01HSV1Q4YY2WAEQFWQ1S66WDJ4. Remember do not copy the quotes with this. Just the contents and paste it in the quotes provided. Switch over to the other tab that has the store microservice i.e. post 80001. Paste the id in the appropriate place and specify the ammount of the product you want like this
<img width="748" alt="image" src="https://github.com/coughlinalbert1/fastapi-react-webapp/assets/111651444/ed494995-3591-4f4e-81a3-c1a71e19ea79">

Execute the request. If you look back at the code in the store microservice, we make a request to another port which is where the warehouse microservice is running. Warehouse goes into the redis db and looks for the product, if it exists, it responds with the product. Now once store gets the response, it creates a new entry in the db for product. Calulates price and all that stuff. Once saved, a background task is made to change the satus from pending to complete if everything is ok.
<img width="748" alt="image" src="https://github.com/coughlinalbert1/fastapi-react-webapp/assets/111651444/09eb2397-796b-4441-bad8-0d6ee286fe60">



Remember the pain and suffering we went through by running the scripts in a separate terminal? Well that comes into play here. Kinda. So theoretically, let's imagine that once you make an order, the product gets deleted at the same time. The two scripts that are running are listening for this scenario. If they detect this, a refund will be issued to the order. 
<img width="1516" alt="image" src="https://github.com/coughlinalbert1/fastapi-react-webapp/assets/111651444/a840d498-e61d-4426-8b18-9ec9f536b789">
Once I created the order, I immediately deleted the product. We can see in the terminal for fastapi-store it changed the status to refunded.
<img width="945" alt="image" src="https://github.com/coughlinalbert1/fastapi-react-webapp/assets/111651444/7aa5524f-43cc-486a-990c-3a796ba2a1a7">




