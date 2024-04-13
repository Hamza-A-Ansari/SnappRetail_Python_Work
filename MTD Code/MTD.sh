#! /bin/bash

screen -d -m -S PSO
echo "screen created"

screen -S PSO -X -p 0 stuff $'cd /home/hansari/pso-dashboard\n'
screen -S PSO -X -p 0 stuff $'. /home/aabedi/anaconda3/bin/activate tableau_email \n'

#screen -S FT.DB -X -p 0 stuf  $'conda activate tableau_email\n'

echo "environment activated"

#screen -S FT.DB -X -p 0 stuff $'which python\n'
screen -S PSO -X -p 0 stuff $'python /home/hansari/pso-dashboard/main.py\n'
echo "script started"

screen -S PSO -X -p 0 stuff $'process_id=$!\n'
screen -S PSO -X -p 0 stuff $'wait $process_id\n'
screen -S PSO -X -p 0 stuff $'exit\n'
echo "script completed"

