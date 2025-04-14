#!/bin/bash

# Install required packages in the container
podman exec postscore_api pip install python-jose[cryptography] passlib[bcrypt] python-multipart

# Restart the app
podman compose restart app

echo "Packages installed and app restarted." 