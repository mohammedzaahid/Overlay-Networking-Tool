This program is designed in Python environment. For the capturing stream, and then output will be stored in Influxdb directly and monitor in Grafana.
Installation:

1.Install automake
		sudo apt-get install automake
  Install autoconf
		sudo apt-get install autoconf
  Install libqd-dev
		sudo apt-get install libqd-dev
  

2.Then you need to install DPMI_Utils
		git clone https://github.com/DPMI/libcap_utils.git
		cd libcap_utils
		autoreconf -si
		mkdir build && cd build
		../configure
		make && make install


3. Next Install Consumer-Bitrate.
		git clone https://github.com/DPMI/consumer-bitrate.git
		cd consumer-bitrate
		make && make install

4.install pip:
		
		sudo apt-get install python-pip python-dev
		sudo pip install --upgrade pip 


5.install influxdb as shown bellow

		curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
		source /etc/lsb-release
		echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
		sudo apt-get update && sudo apt-get install influxdb
		sudo pip install influxdb

6.install Grafana as shown bellow

		wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_4.4.3_amd64.deb 
		sudo apt-get install -y adduser libfontconfig 
		sudo dpkg -i grafana_4.4.3_amd64.deb

7.install Flask as shown bellow
		sudo pip install Flask



8. Rest Api Usage:

a. After installating all the above system requirements, please change the settings(variables) before starting the api.
	change the (interface) "eth_val".
	create the database and chanege the database in "influx_db".
	change the username as required in variable "user_name". In my case user_name is stark
	change the password as required in variable "pass_word". In my case pass_word is stark
	

This tool is designed for calculating
                1. Consumer-Bitrates.
These values are plotted in Grafana by grouping technique.
RestApi manual:

#########Here my username:password is stark:stark

we are provided different facilities to analyse stream statistics.
1.Run stream
		curl -u username:password http:/localhost:5000/run/<stream>
2.Change stream
		curl -u username:password http:/localhost:5000/change/<stream>
3.Stop stream
		curl -u username:password http:/localhost:5000/stop
4.Show active streams
		curl -u username:password http:/localhost:5000/show
5.Add stream
		curl -u username:password http:/localhost:5000/add/<stream>
6.Delete stream
		curl -u username:password http:/localhost:5000/delete/<stream>


Next run the python api.py file in consumer-bitrate folder.

b. Grafana

1. Add the influx database to the datasource in Grafana, to display the output

2. Create the dashbord and use the above database, use the tags "Dynamic_tag" automatically displayed with the running steams.
3. Use 'distinct' as aggregration and "bitrate" as measurements
