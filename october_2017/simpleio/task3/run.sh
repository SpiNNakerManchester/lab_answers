!#/bin/bash

python sender.py inputSpikes_1 19998 &
sender_pid=$!
python receiver.py pop_1 19997 &
receiver_pid=$!
python script.py 19998 19997

kill $sender_pid
kill $receiver_pid
