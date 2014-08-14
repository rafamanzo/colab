#! /bin/bash

# Make sure rvm is installed under sudo user
sudo bash -c "curl -L get.rvm.io | bash -s stable"

# Set rvm on the PATH and install ruby 2.0.0
sudo bash -c "source /usr/local/rvm/scripts/rvm && rvm install ruby-2.0.0"
sudo bash -c "source /usr/local/rvm/scripts/rvm && rvm gemset create gitlab"
sudo bash -c "source /usr/local/rvm/scripts/rvm && rvm gemset create redmine"

sudo bash -c "source /usr/local/rvm/scripts/rvm && rvm use 2.0.0@gitlab --default"
sudo bash -c "source /usr/local/rvm/scripts/rvm && gem install bundler --no-ri --no-rdoc"
