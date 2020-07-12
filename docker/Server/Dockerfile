FROM node:latest

ENV APP_PATH /Lyricae/app

RUN mkdir $APP_PATH
WORKDIR $APP_PATH

echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
CMD npm run start

EXPOSE 3000