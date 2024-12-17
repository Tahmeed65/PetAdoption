## Docker instructions for backend
- `cd backend`
- `docker build -t project .`
- `docker run -d -p 5002:5000 project`

## Docker instructions for frontend
- `cd ..` (if coming from the last step)
- `cd frontend`
- `docker build -t project-frontend .`
- `docker run -d -p 5001:5001 project-frontend`

## Using the site
- Go to http://localhost:5001 to view website
- A fake username with no data is `ILoveCats1996`, password is `kitten10006`
- A fake admin username is `EricPetfinderAdmin`, password is `unbreakablePassword`
- A fake username with data already is `JohnAdopter`, password is `password123`

## Figma 
https://www.figma.com/design/AvnZdzKFQ5ocd2BMVNHUT2/cse2102-group-project?node-id=0-1&t=ljKhrMpYmPsV3Vo7-1
