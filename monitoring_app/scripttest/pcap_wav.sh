#!/bin/bash
pa=$(python bb.py $1)
pcap=$1
law='a-law'
var="ssrc"
rep="${pa//[^var]}"
n="${#rep}"
i=0
for (( i=0; i<n; i++ )) ; do
    l="${#pa}"
    i0=$(expr index "$pa" "\'")
    pa="$(echo "$pa" |cut -c$(expr $i0 + 1 )-$(expr $l))"
    i1=$(expr index "$pa" "=")
    i2=$(expr index "$pa" "'")
    ssrc="$(echo "$pa" |cut -c$(expr $i1 + 1 )-$(expr $i2 - 1 ))"
    echo "$pcap.$ssrc.wav"
    rm -f $pcap.$ssrc.raw $pcap.$ssrc.wav
    sudo tshark -n -r $pcap -2R "rtp && rtp.ssrc == $ssrc" -T fields -e rtp.payload | sed "s/:/ /g" | perl -ne 's/([0-9a-f]{2})/print chr hex $1/gie' >>  $pcap.$ssrc.raw
    sox -t raw -r 8000 -v 4 -c 1 -e $law $pcap.$ssrc.raw $pcap.$ssrc.wav
    pa="$(echo "$pa" |cut -c$(expr $i2 + 1 )-$(expr $l))"
    if [[ "$pa" == "]" ]];
    then
       i=n;
    fi

       
        
done

