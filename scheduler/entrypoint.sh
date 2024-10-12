echo "Container starting at $(date +%H:%M:%S)"
cron && tail -f /scheduler/logfile.log
