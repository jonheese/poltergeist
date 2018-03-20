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
### Using the automatic deploy script (`deploy.sh`)
1. Check out this project:
    ```
    $ git clone git@code.viawest.net:jon.heese/poltergeist.git
    ```
2. Copy your desired mp3 file, named `<sitename>.mp3`, to the `webdirs` directory:
    ```
    $ cp newsite.mp3 webdirs/
    ```
3. **Optional:** Copy a `jpg`/`png` file, named `<sitename>.[jpg|png]`, to the `webdirs` directory, if you want an image to display on the page:
    ```
    $ cp newsite.png webdirs/
    ```
4. Run the addsite.sh script:
    ```
    $ ./addsite.sh
    Enter site name: newsite
    Enter page title: New Title!
    Do you have any customizations to make before commit/push? [y/N]:
    ```
5. If you want to make any further customizations to make before committing (eg. any special logic in the `index.php` or something), enter `y`, make those changes, then commit, push, deploy (see below).
6. If you have no further customizations to make, enter `n` and the script will automatically commit, push, and deploy the code to the Raspberry Pis.

**NOTE:** The `deploy.sh` script uses SSH to deploy the code to any remote device(s), so you will either need to have SSH key auth set up, or type in the SSH password for your current user (key auth is highly recommended).

**NOTE:** In the case of inetu-hdmi13 and inetu-hdmi19 (the Raspberry Pis in Platform Engineering and ACT), they will automatically pull any changes pushed to this Gitlab project on 5-minute intervals, so you do not need to deploy directly to them if you are patient enough.

### Manual Deploy Steps ###
If you had additional customizations to be made before committing in the steps above, you can commit, push, and deploy with the following commands:
```
git add .
git commit -a
git push -u origin master
./deploy.sh
```
