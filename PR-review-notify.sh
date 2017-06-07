#!/bin/bash

source ~/.bash_profile;
pyenv activate nelp-github-webhook;
python /home/nelp/github-webhooks/PR-review-notify.py;

