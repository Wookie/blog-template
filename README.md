## LPo Blog Template

This is the blog template that I use for [my blog](http://blog.linuxprogrammer.org).  Since I use it only for blogging, I customized the macros.py file that [poole.py](https://bitbucket.org/obensonne/poole) uses to support blogging.

The page.html file uses [foundation](http://foundation.zurb.com/) to be HTML5 and responsive.  It also uses [Font Awesome](http://fortawesome.github.io/Font-Awesome/) mostly because Font Awesome has a Bitcoin symbol character.

I use git as my publishing tool.  The included post-recieve script handles running poole and deploying the files to the web root of my hosted webserver.  Setting this up on your server is easy:

# First create an acccount on your webserver for deploying to your webserver.
# Create a bare repo in the home directory of the deploy user account.
# Edit the post-receive script to match your site (e.g. changet the base-url passed to pool and adjust the folders for where your webserver serves files from).
# Set up the permissions of your webserver root and deploy user so that the deploy user is able to write files into the directory.
# Write some blog posts in the input directory.
# Commit the blog posts and push to the remote repo on your web server.
# The post-receive script should run after your commit and handle running poole.py to generate the new version of your site and then deploy it.

The post-receive script deploys files using atomic operations so that the deploy cannot break the site.  The version last step is an atomic overwrite of the symbolic link to the folder for the newest version of your site.  So either the full deploy works or it doesn't.  When this post-receive script runs it does the following:

# Clones the master branch to a .tmp dir.
# Executes poole.py on the .tmp dir.  This generates the new version of your site in .tmp/output.
# It gets the short hash value for the revision and uses that as the name of the deploy folder in a .versions folder outside of the webserver's web root.
# After fixing up permissions on the folders, it makes a backup copy of the symbolic link to the previous version.
# Then it atomically changes the symbolic link for the web root to point to the new version of the site.
# It then fixes permissions on the symbolic links.

You'll notice that the post-receive script uses sudo for most of the commands.  I use the sudoers file to limit the commands that the deploy user can run.  In my sudoers file I have:

    Cmnd_Alias DEPLOY=/bin/ls, /bin/cp, /bin/mv, /bin/mkdir, /bin/chown, /bin/chmod, /bin/rm, /bin/ln, /usr/bin/git, /etc/init.d/nginx
    deploy-user    ALL=NOPASSWD: DEPLOY

The name of the user account that does the deploying is 'deploy-user'.  This is necessary so that the web server can run under a user and group other than the deploy user.  Keeping the webserver process limited in what it can do on the system.

