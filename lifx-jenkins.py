#!/usr/bin/env python
import json
import sys
import time
import urllib
from multiprocessing import Process

from lifxlan import LifxLAN, YELLOW, RED, BLUE, COLD_WHITE


def main():
    jenkins_job_url = None

    if len(sys.argv) != 2:
        print "Usage: python lifx-jenkins.py [path-to-jenkins-job]"
        return

    jenkins_job_url = "%s/api/json" % sys.argv[1]
    print "Watching the following Jenkins job JSON: %s..." % jenkins_job_url

    num_lights = 1
    print "Discovering lights..."
    lifx = LifxLAN(num_lights)
    devices = lifx.get_lights()
    print "\nFound {} light(s):\n".format(len(devices))

    # Using the first bulb it finds.
    bulb = devices[0]
    print bulb

    poll_interval = 5

    def set_color_yellow():
        bulb.set_power("on")
        bulb.set_color(YELLOW)

    def set_color_red():
        bulb.set_power("on")
        bulb.set_color(RED)

    def set_color_blue():
        bulb.set_power("on")
        bulb.set_color(BLUE)
    
    def set_color_aborted():
        bulb.set_power("on")
        bulb.set_color(COLD_WHITE)

    def setColorYellowAnime():
        while True:
            set_color_yellow()
            print 'Bulb on'
            time.sleep(1)
            bulb.set_power("off")
            print 'Bulb off'
            time.sleep(1)

    def setColorRedAnime():
        while True:
            set_color_red()
            print 'Bulb on'
            time.sleep(1)
            bulb.set_power("off")
            print 'Bulb off'
            time.sleep(1)

    def setColorBlueAnime():
        while True:
            set_color_blue()
            print 'Bulb on'
            time.sleep(1)
            bulb.set_power("off")
            print 'Bulb off'
            time.sleep(1)

    def setColorAbortedAnime():
        while True:
            set_color_aborted()
            print 'Bulb on'
            time.sleep(1)
            bulb.set_power("off")
            print 'Bulb off'
            time.sleep(1)

    process_set_color_yellow_anime = None
    process_set_color_red_anime = None
    process_set_color_blue_anime = None
    process_set_color_aborted_anime = None

    print 'Watching URL: %s' % (jenkins_job_url)

    last_color = 'blue'
    set_color_blue()

    while True:
        response = urllib.urlopen(jenkins_job_url)
        data = json.loads(response.read())
        color = data['color']
        print 'Current color of Jenkins job: %s' % (color)

        if color != last_color:
            print 'State changed from %s to %s' % (last_color, color)
            last_color = color

            if process_set_color_yellow_anime:
                if process_set_color_yellow_anime.is_alive():
                    process_set_color_yellow_anime.terminate()

            if process_set_color_red_anime:
                if process_set_color_red_anime.is_alive():
                    process_set_color_red_anime.terminate()

            if process_set_color_blue_anime:
                if process_set_color_blue_anime.is_alive():
                    process_set_color_blue_anime.terminate()

            if process_set_color_aborted_anime:
                if process_set_color_aborted_anime.is_alive():
                    process_set_color_aborted_anime.terminate()

            if color == 'yellow':
                set_color_yellow()
            elif color == 'red':
                set_color_red()
            elif color == 'blue':
                set_color_blue()
            elif color == 'aborted':
                set_color_aborted()
            elif color == 'yellow_anime':
                process_set_color_yellow_anime = Process(target=setColorYellowAnime)
                process_set_color_yellow_anime.start()
            elif color == 'red_anime':
                process_set_color_red_anime = Process(target=setColorRedAnime)
                process_set_color_red_anime.start()
            elif color == 'blue_anime':
                process_set_color_blue_anime = Process(target=setColorBlueAnime)
                process_set_color_blue_anime.start()
            elif color == 'aborted_anime':
                process_set_color_aborted_anime = Process(target=setColorAbortedAnime)
                process_set_color_aborted_anime.start()

            response.close()

        time.sleep(poll_interval)


if __name__=="__main__":
    main()
