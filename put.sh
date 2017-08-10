#!/bin/bash


topic=('nl.ams.boven' 'nl.ams.midden' 'nl.ams.beneden' 'nl.ams.uat' 'nl.ams.test' 'nl.ams.dev')
stat=('INFO Dit is een test' 'WARN No koffee' 'WARN Disk 70% full ' 'ERROR Disk 100% full' 'ERROR System down' 'OK All UP' 'OK Logged in' 'OK done' 'WARN example mesage' 'OK')


while true; do
  t=$(((RANDOM % ${#topic[@]})))
  s=$(((RANDOM % ${#stat[@]})))
  n=$(((RANDOM % 3)+1))
  z=$(((RANDOM % 5)))
  echo "${topic[${t}]}${n} ${stat[${s}]}"  > /dev/tcp/localhost/5000
  echo "${topic[${t}]}${n} enable 1"  > /dev/tcp/localhost/5000
  echo "${topic[${t}]}${n} timeout 60"  > /dev/tcp/localhost/5000
  sleep ${z} 
done

