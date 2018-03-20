# Poltergeist
Makes TVs talk to you

## Installation
```
git clone git@code.viawest.net:jon.heese/poltergeist.git
cd poltergeist
# create config-local.conf as documented in config.conf
vi config-local.conf
./deploy.sh
```

## Adding your own content
1. Check out this project:
   `$ git clone git@code.viawest.net:jon.heese/poltergeist.git`
2. Copy an mp3 file, named `<sitename>.mp3`, to the `webdirs` directory:
   `$ cp newsite.mp3 webdirs/`
3. Optional: Copy a `jpg`/`png` file, named `<sitename>.[jpg|png]`, to the `webdirs` directory, if you want an image to display on the page:
   `$ cp newsite.png webdirs/`
3. Run the addsite.sh script:
```
$ ./addsite.sh
Enter site name: newsite
Enter page title: New Title!
Do you have any customizations to make before commit/push? [y/N]:
```
4. If you want to make any further customizations to make before committing (eg. any special logic in the `index.php` or something), enter `y`, make those changes, then commit, push, deploy (see below).
5. If you have no further customizations to make, enter `y` and the script will automatically commit, push, and deploy the code to the Raspberry Pis.

### Manual Deploy Steps ###
If you had additional customizations to be made before committing in the steps above, you can commit, push, and deploy with the following commands:
```
git add .
git commit -a
git push -u origin master
./deploy.sh
```
