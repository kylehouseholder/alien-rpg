# Setup of a remote workspace/dev environment
- We want you to have access to the Linux server for coding/testing
	- By using a Secure Shell (SSH) key we prevent you from needing a password, which is more secure than sending a password out over the internet
- Bot run only one instance at a time, to avoid Discord conflicts/banning
- We will use tmux (Terminal Multiplexer) to share the bot session


## Step 1: Generate an SSH Key
From a  command line, enter (Windows and MacOS):

```
ssh-keygen -t ed25519 -C "your-email@change-this.com"
```

This should put both a private and public key into your .ssh dir.
	- On Windows, this should be C:\Users\your_username\.ssh\
	- On Mac, this should be ~/.ssh/

The PRIVATE key is untouched, and becomes the thing your machine's SSH client will use to try and connect to a remote machine.

## Step 2: Login to remote machine

The PUBLIC key's contents (text inside the file) will be sent to the remote machine and stored there under your username. To accomplish this:

```
ssh -p 772 ztrob@160.79.95.118
```

This attempts to connect via secure shell to port 772, user ztrob, at the remote machine. It will prompt you for your password.

Once you're logged in, you should be able to navigate to:
	- ~/.ssh/authorized_keys

This file will hold the pasted contents of your generated file on your current machine.

## Step 3: Authorize yourself!

On the local machine (the one you are physically touching), you need to open the public keyfile and retrieve the contents. The file should be (in your .ssh dir) called id_ed25519.pub, and will look like:

```
ssh-ed25519 AAAAC3NzaC1lZ9Ul4JxXj9ZdjfIS438DLHWqW theuselessuser@gmank.com
```

The single line you find on your local machine is all you should need to put inside the remote machine's authorized_keys file, and now you will no longer need a password when you ssh in.

### NOTES:

Cursor (or any other third party ssh client) should by default be pointed at your standard .ssh dir under your machine's username. On Mac or Linux, "~" points at your user's home dir (/home/ztrob/) and is a shorthand for referencing it.

To configure remote hosts in Cursor:
- Ctrl + Shift + P to access the command bar (or click it)
- Type "> SSH config" and you should see an option for your local SSH dir. Select it.
- Your remote can be named whatever you like, here's an example:
```
Host whateverYouWannaCallIt
  HostName 160.79.95.118
  User ztrob
  Port 772
  ```

