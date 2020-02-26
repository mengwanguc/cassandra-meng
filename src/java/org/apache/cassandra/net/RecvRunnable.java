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

import java.io.InputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.nio.ByteBuffer;

import org.apache.cassandra.db.ReadCommand;
import org.apache.cassandra.service.ReadCallback;
import org.apache.cassandra.tracing.Tracing;


public class RecvRunnable implements Runnable {
	public MessageOut<ReadCommand> message;
	public InetAddress endpoint;
	public int id;
	
	public RecvRunnable(MessageOut<ReadCommand> message, InetAddress endpoint, int id) {
		this.message = message;
		this.endpoint = endpoint;
		this.id = id;
	}
	
	public void run() {
		OutboundTcpConnection connection = MessagingService.instance().getConnectionPool(endpoint).getConnection(message);
		Socket socket = connection.getSocket();
		if (socket != null) {
	        try {
	            long startTime = System.nanoTime();
	        	InputStream in = socket.getInputStream();
	        	int n = in.read();
	        	
	        	if (n == -16) {
	                long endTime = System.nanoTime();
	                long latency = endTime - startTime;
	                double latencyDouble = ((double) latency) / 1000000;
	        	    
	                
//	                System.out.println("        @meng: RecvRunnable have waited for " + Double.toString(latencyDouble) + "ms");
	        	    
	                CallbackInfo callbackInfo = MessagingService.instance().removeRegisteredCallback(id);
	                if (callbackInfo == null)
	                    return;
	                
	                IAsyncCallback cb = callbackInfo.callback;
	                if (cb instanceof ReadCallback) {
	                    System.out.println("    @meng: " + System.currentTimeMillis() + " - " 
	                            + Long.toString(((ReadCallback) cb).getExecutor().getCommandCounter()) 
	                            + " - Request is Mittcpu Reject from " + socket.getRemoteSocketAddress().toString()
	                            + " after " + Double.toString(latencyDouble) + "ms");
	                    ((ReadCallback) cb).onMittcpuRejection();
	                }
	        	}
	        } catch (Exception e) {
	            System.out.println("   @meng: error when trying to get Mittcpu rejection:");
	        	System.out.println(e.getStackTrace());
	        }
	        
		}
		
	}
	
	
}


