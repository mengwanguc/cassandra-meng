/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.cassandra.net;

import java.io.IOException;
import java.io.InputStream;
import java.net.InetAddress;
import java.net.Socket;

import org.apache.cassandra.db.ReadCommand;


public class RecvRunnable implements Runnable {
	public MessageOut<ReadCommand> message;
	public InetAddress endpoint;
	
	public RecvRunnable(MessageOut<ReadCommand> message, InetAddress endpoint) {
		this.message = message;
		this.endpoint = endpoint;
	}
	
	public void run() {
		OutboundTcpConnection connection = MessagingService.instance().getConnectionPool(endpoint).getConnection(message);
		Socket socket = connection.getSocket();
		if (socket != null) {
	        try {
	        	InputStream in = socket.getInputStream();
	        	System.out.println("		@@@meng: inputstream's class name: " + in.getClass().getName());
	        	System.out.println("		@meng: Starting to read...");
	        	int c = in.read();
	        	
	        } catch (IOException e) {
	        	System.out.println(e.getStackTrace());
	        }
	        
		}
		
	}
	
	
}


