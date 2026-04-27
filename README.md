
<h1 align="center">PortSight</h1>

<p align="center">
  A simple and clean terminal-based TCP port scanner built with Python.
</p>


<hr>

<h2>About</h2>

<p>
PortSight is a small Python project that scans common TCP ports on a target IP address
and shows which ports are open. It was built with a focus on simplicity, readable output,
and real usefulness instead of unnecessary complexity.
</p>

<p>
The tool runs directly in the terminal, asks for a target IP, scans the default range,
and presents results in a neat format.
</p>

<hr>

<h2>Features</h2>

<ul>
  <li>Scans ports 1 to 1024 by default</li>
  <li>Fast multithreaded scanning</li>
  <li>Clean terminal interface</li>
  <li>Detects common services (HTTP, SSH, DNS, etc.)</li>
  <li>Shows response time for open ports</li>
  <li>Simple and beginner-friendly codebase</li>
  <li>No external libraries required</li>
</ul>

<hr>

<h2>How It Works</h2>

<p>
PortSight uses TCP connect scanning. It attempts to establish a connection to each port
in the selected range. If the connection succeeds, the port is considered open.
</p>

<p>
This makes it a good learning project for networking, sockets, threading, and Python basics.
</p>

<hr>

<h2>Installation</h2>

<pre>
git clone https://github.com/ayaanable/PortSight.git
cd PortSight
python portsight.py
</pre>

<hr>

<h2>Usage</h2>

<p>Run the file:</p>

<pre>
python portsight.py
</pre>

<p>Then enter the target IP address when prompted:</p>

<pre>
Target IP : 192.168.1.1
</pre>

<hr>

<h2>Example Output</h2>

<pre>
PortSight

Target IP : 192.168.1.1

Open Ports

22    ssh        4.2 ms
80    http       2.1 ms
443   https      3.0 ms
</pre>

<hr>

<h2>Why I Made This</h2>

<p>
I wanted to build something more practical than a typical beginner project.
PortSight helped me learn how sockets work, how multithreading improves speed,
and how to design terminal tools that feel clean and usable.
</p>


<hr>

<h2>Future Improvements</h2>

<ul>
  <li>Custom port ranges</li>
  <li>UDP scanning</li>
  <li>Service banner grabbing</li>
  <li>Save results to file</li>
  <li>OS detection basics</li>
</ul>

<hr>



<p>
Made with Python and curiosity.
</p>

