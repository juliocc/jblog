jblog is a simple Django blog for Google App Engine.

Run locally:

    git clone git@github.com:potatolondon/djappengine.git
    cd djappengine
    dev_appserver .

Visit <http://localhost:8000>.

Now deploy to appspot, first set up an app on <http://appengine.google.com> and replace `application` in `app.yaml` with the name of your app (in your text editor or like this):

    sed -i '' 's/djappeng1ne/myappid/' app.yaml

You're ready to deploy:

    appcfg.py update .
