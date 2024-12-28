To avoid having a request stopped by the reddit server, we avoid too much spam, by waiting 5 seconds before sending 4 new requests, moreover if they conflict, we make them wait to make a new try later (1/5s) in their own thread. The number of requests and waiting time is to be adjusted according to your connection and the blocked requests.
(each thread has a lifespan of 1 minute. Be careful, I saw an error that prevented the thread from closing correctly)
- To modify: the waiting time for the closing of all threads is done once the list of urls is completed, all threads can close alone once they have completed their task, but those that bug can only do so once the list is processed.
-Those that bug can also never close => to see for what?
- /!\ Line 32 => ydl.extract_info(url, download=False) creates an infinite loop error and prevents the thread from closing properly despite the requested interruption, I still haven't found the solution.
-- idea -> maybe it doesn't find the requested format in the link and searches in a loop
--another idea -> too many associated sub-links 
