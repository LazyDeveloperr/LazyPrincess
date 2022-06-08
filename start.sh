if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/LazyDeveloperss/test9.git /test9
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /test9
fi
cd /test9
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
