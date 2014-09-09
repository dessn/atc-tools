#!/bin/sh

atc.py delete observatory GTC      
atc.py delete observatory AAT      
atc.py delete observatory SALT     
atc.py delete observatory HET      
atc.py delete observatory KECK     
atc.py delete observatory NTT      
atc.py delete observatory MAGELLAN 
atc.py delete observatory MDM      
atc.py delete observatory LBT      
atc.py delete observatory GEMINI-S 
atc.py delete observatory GEMINI-N
atc.py delete observatory VLT      
atc.py delete observatory MMT

atc.py create observatory GTC      --name="Gran Telescopio Canarias (10.4m)"    --longitude=-17:53:31.3  --latitude=+28:45:23.8 --altitude=2275
atc.py create observatory AAT      --name="Anglo-Australian Telescope (3.9m)"
atc.py create observatory SALT     --name="South African Large Telescope (10m)" --longitude=+20:48:38.4  --latitude=-32:22:33.6 --altitude=1798
atc.py create observatory HET      --name="Hobby-Eberly Telescope (9.2m)"       --longitude=-104:00:53.0 --latitude=+30:40:53.2 --altitude=2026
atc.py create observatory KECK     --name="Keck Observatory (10m)"              --longitude=-155:28:28.1 --latitude=+19:49:35.0 --altitude=4160
atc.py create observatory NTT      --name="New Technology Telescope (3.6m)"     --longitude=-70:44:01.5  --latitude=-29:15:32.1 --altitude=2375
atc.py create observatory MAGELLAN --name="Magellan Telescopes (6.5m)"          --longitude=-70:41:32.6  --latitude=-29:00:51.0 --altitude=2516
atc.py create observatory MDM      --name="MDM Observatory (2.4m)"              --longitude=-111:37:00   --latitude=+31:57:00   --altitude=1939
atc.py create observatory LBT      --name="Large Binocular Telescope (2x8.4m)"  --longitude=-109:53:09   --latitude=+32:42:05   --altitude=3182
atc.py create observatory GEMINI-S --name="Gemini South (8.1m)"                 --longitude=-70:44:11.7  --latitude=-30:14:26.6 --altitude=2722
atc.py create observatory GEMINI-N --name="Gemini North (8.1m)"                 --longitude=-155:28:11.4 --latitude=+19:49:26.3 --altitude=4213
atc.py create observatory VLT      --name="Very Large Telescope (4x8.2m)"       --longitude=-70:24:15    --latitude=-24:37:38   --altitude=2635
atc.py create observatory MMT      --name="MMT (6.5m)"                          --longitude=-110:53:06   --latitude=+31:41:18   --altitude=2606
