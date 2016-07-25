---
layout: post
title:  "Forward Secrecy with Symmetric Cryptography?"
date:   2016-07-08 22:05:59 +0200
categories: jekyll update
---
In cryptography, <em>forward secrecy</em> is a property of key establishment protocols. The <a href="http://cacr.uwaterloo.ca/hac/">Handbook of Applied Cryptography</a> (HoAC) defines a protocol to have forward secrecy if the compromise of long-term secrets (e.g. long-term keys) does not compromise past session keys. In other words, all previous sessions – e.g. past communication sessions with an online banking site or an online store like Amazon – remain securily locked in the past. It should be noted that this post refers to the forward secrecy property of cryptographic key establishment protocols; forward secrecy in the context of random number generators is a different topic.

Intuitively, in the context of key establishment protocols, the term <em>forward secrecy</em> is somewhat misleading since it has the word <em>forward</em> in it, but actually says something about the <em>past</em> sessions. Basically, the idea behind forward secrecy is that the entire message traffic <em>prior</em> to the compromise of the long-term key(s) cannot be easily decrypted by the attacker, i.e. the traffic is locked securily in the past. Here, ‘easily’ means that the attacker cannot efficiently decrypt the traffic unless she knows a polynomial-time algorithm for solving the underlying mathematical problem of the cryptographic scheme, e.g. an algorithm for solving the Diffie-Hellman Problem (DLP) for the Diffie-Hellman (DH) key agreement protocol. Problems like DLP are believed to be computationally intractable – NP-hard in the complexity theory parlance – because since decades (DH, for instance, was introduced in 1976), no one was able to come up with an efficient method to solve them. That is essentially the reason why such problems form the basis of widely used modern cryptographic protocols like TLS.

# Why Woul You Want to Have Forward Secrecy?
Imagine two embassies exchanging messages on political matters. To ensure confidentiality, the embassies encrypt their communication sessions using session keys. Obviously, it would be disastreuous if an attacker, say another nation state, could read the messages transmitted during <em>all</em> previous sessions just by compromising a single long-term key.

With forward secrecy, the attacker has to spend the same amount of work to decrypt <em>any single</em> previous session. In other words, even if the attacker succeeds in compromising the long-term key, she has to spend the same -- practically infeasible -- effort to decrypt any previous session as if she had no knowledge of the long-term key.

For a more day-to-day example, assume the private key of a service like Gmail or Twitter gets compromised. Even if the compromise is noted by the service provider, without forward secrecy the attackers can read all previous sessions of every user. And there’s nothing <em>you</em> can do about it, because the works even if your own machine is perfectly secure. With forward secrecy, even if an adversary is currently recording all Twitter users' encrypted traffic, and later cracks or steals Twitter’s private keys, the attacker [won't be able to use those keys to decrypt the recorded traffic](https://blog.twitter.com/2013/forward-secrecy-at-twitter-0).

# The Definition Zoo
There seems to exist a definition zoo for forward secrecy. Compared to other some other topics, the forward secrecy zoo is quite small. Nonetheless, the subtle differences in the definitions <em>do</em> lead to confusion and heated debates whether a certain scheme has forward secrecy or not.

According to the <a href="http://cacr.uwaterloo.ca/hac/">Handbook of Applied Cryptography</a> by Menezes, van Oorschot, and Vanstone, a protocol is said to have forward secrecy if compromise of long-term keys does not compromise past session keys. The discussion of the definition goes on to explain how forward secrecy can be achieved (namely, using the <a href="https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange">Diffie-Hellman key agreement</a>) and that, if long-term keys are compromised, future sessions are (nonetheless) subject to impersonation by an active adversary.

Noteworthy is that the above definition assumes an <em>active</em> attacker. This assumption implies that the compromise of long-term keys <em>always</em> leads to a complete break of the key exchange scheme. Because the adversary is allowed to impersonate any of the compromised parties, she can always actively participate in the key agreement phase and thus retrieve that specific session key.

In Security Engineering, Ross Anderson introduces the notion of forward secrecy under the name <em>forward security</em>. Anderson starts by introducing autokeying, a mechanism where two or more parties who share a key hash it at agreed times with the messages they have exchanged since the last key change: <em>Ki+1=h(Ki,Mi1,Mi2,…)</em>. If an attacker compromises one of the parties and steals their key, then as soon as the legitimate parties exchange a message which the attacker doesn’t observe or guess, the attacker can no longer decrypt their traffic (i.e. the security is restored). Anderson refers to this property as <em>forward security</em> mentioning that the use of asymmetric crypto allows a slightly stronger form of forward security. Namely, that as soon as a compromised party exchanges a message with an uncrompromised one which the opponent doesn’t control, the security can be recovered even if the message is in plain sight.

In <a href="http://cacr.uwaterloo.ca/~dstinson/CTAP.html">Cryptography: Theory and Practice</a>, Stinson defines a key exchange scheme to have the forward secrecy property if the attacker cannot learn the values of previous session keys. Stinson describes scenarios where the adversary learns the value of a particular session key or the long-term keys of one or more participants. Now the purpose of forward secrecy according to Stinson is to limit the damage that is done in these types of attacks.

The <a href="https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102.pdf?__blob=publicationFile&amp;v=2">BSI Technical Guideline on Cryptographic Mechanisms and Key Lengths</a> defines forward secrecy as a property of a key exchange protocol where an attacker who knows (i.e. obtained in some way) the long-term secrets of one or both communicating parties, is not able to determine the session key for any session she has not compromised.

The BSI definition is [...]

In <a href="http://eprint.iacr.org/2005/176.pdf">HMQV: A High-Performance Secure Diffie-Hellman Protocol</a>, Krawczyk presents HMQV – a variant of the MQV protocol – that provides the same performance and functionality, but for which all the MQV’s security goals can be formally proved in the random oracle model (under the computational Diffie-Hellman assumption). For the HMQV protocol, Krawczyk introduced the notion of <em>weak forward secrecy</em>.

<p>As summarized by <a href="https://www.cs.ox.ac.uk/people/cas.cremers/downloads/papers/CrFe2012-eckpfs.pdf">Cremers and Feltz</a>, Krawczyk sketches a generic attack where the adversary actively interferes with the legitimated communicating parties by injecting self-constructed messages. This enables her to compute the session key if she later learns the long-term secret keys of the parties. When the long-term keys are compromised, the weak forward secrecy property guarantees that previously established session keys remain secret, but only for sessions in which the adversary did not actively interfere.</p>

<p>The notion of weak forward secrecy turns out to be interesting in applied cryptography, because in practice mounting an active attack is much harder than simply recording past communications, and, as a result, can typically be performed on a smaller number of sessions.</p>

<h1 id="can-you-achieve-forward-secrecy-without-asymmetric-crypto">Can you achieve forward secrecy without asymmetric crypto?</h1>
<p>The short answer is: it depends. It depends on the definition you choose, that is.</p>

<p>Forward secrecy is typically associated with Public Key Cryptography (PKC) and, in particular, with key agreement schemes based on PKC like the <a href="https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange">Diffie-Hellman key agreement</a>. Achieving forward secrecy in such protocols requires that the session keys do not depend on the long-term secret as discussed in <a href="http://link.springer.com/chapter/10.1007/978-3-540-46588-1_29">Forward Secrecy and Its Application to Future Mobile Communications Security</a> by Park, Boyd, and Moon. Moreover, forward secrecy in key agreement protocols can only be achieved if the ephemeral keys are generated using a random number generator that guarantees the <a href="https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Zertifizierung/Interpretationen/AIS_31_Functionality_classes_for_random_number_generators_e.pdf">enhanced backward secrecy</a> (see the <a href="https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102.pdf?__blob=publicationFile&amp;v=2">BSI Technical Guideline on Cryptographic Mechanisms and Key Lengths</a> for details).</p>

<p>The fact that the session keys must not depend on the long-term secret implies that there cannot be a symmetric crypto-based key <em>agreement</em> scheme achieving forward secrecy. Nevertheless, according to the definition of forward secrecy in the <a href="http://cacr.uwaterloo.ca/hac/">Handbook of Applied Cryptography</a>, it is possible to achieve using a key <em>update</em> scheme like the one recommended by the <a href="https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102.pdf?__blob=publicationFile&amp;v=2">BSI Technical Guideline on Cryptographic Mechanisms and Key Lengths</a>.</p>

<p>In a key update scheme, the parties synchronuosly update the session key without an explicit communication. In such a setting, the master key <em>K</em> is updated at the time point <em>t</em> by both (or all) communicating parties. For this purpose, the <a href="https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102.pdf?__blob=publicationFile&amp;v=2">BSI Technical Guideline on Cryptographic Mechanisms and Key Lengths</a> recommend the following mechanism.</p>

<p>exchanged since the last key change: <em>Ki+1=h(Ki,Mi1,Mi2,…)</em>.</p>

<figure class="highlight"><pre><code class="language-ruby" data-lang="ruby"><span class="k">def</span> <span class="nf">print_hi</span><span class="p">(</span><span class="nb">name</span><span class="p">)</span>
  <span class="nb">puts</span> <span class="s2">"Hi, </span><span class="si">#{</span><span class="nb">name</span><span class="si">}</span><span class="s2">"</span>
<span class="k">end</span>
<span class="n">print_hi</span><span class="p">(</span><span class="s1">'Tom'</span><span class="p">)</span>
<span class="c1">#=&gt; prints 'Hi, Tom' to STDOUT.</span></code></pre></figure>

<p>Check out the <a href="http://jekyllrb.com/docs/home">Jekyll docs</a> for more info on how to get the most out of Jekyll. File all bugs/feature requests at <a href="https://github.com/jekyll/jekyll">Jekyll’s GitHub repo</a>. If you have questions, you can ask them on <a href="https://talk.jekyllrb.com/">Jekyll Talk</a>.</p>


  </div>

</article>

      </div>
    </div>

    <footer class="site-footer">

  <div class="wrapper">

    <h2 class="footer-heading">Compulogy (Turing incomplete)</h2>

    <div class="footer-col-wrapper">
      <div class="footer-col footer-col-1">
        <ul class="contact-list">
          <li>Compulogy (Turing incomplete)</li>
          <li><a href="mailto:paul.duplys@posteo.de">paul.duplys@posteo.de</a></li>
        </ul>
      </div>

      <div class="footer-col footer-col-2">
        <ul class="social-media-list">
          
          <li>
            <a href="https://github.com/duplys"><span class="icon icon--github"><svg viewBox="0 0 16 16"><path fill="#828282" d="M7.999,0.431c-4.285,0-7.76,3.474-7.76,7.761 c0,3.428,2.223,6.337,5.307,7.363c0.388,0.071,0.53-0.168,0.53-0.374c0-0.184-0.007-0.672-0.01-1.32 c-2.159,0.469-2.614-1.04-2.614-1.04c-0.353-0.896-0.862-1.135-0.862-1.135c-0.705-0.481,0.053-0.472,0.053-0.472 c0.779,0.055,1.189,0.8,1.189,0.8c0.692,1.186,1.816,0.843,2.258,0.645c0.071-0.502,0.271-0.843,0.493-1.037 C4.86,11.425,3.049,10.76,3.049,7.786c0-0.847,0.302-1.54,0.799-2.082C3.768,5.507,3.501,4.718,3.924,3.65 c0,0,0.652-0.209,2.134,0.796C6.677,4.273,7.34,4.187,8,4.184c0.659,0.003,1.323,0.089,1.943,0.261 c1.482-1.004,2.132-0.796,2.132-0.796c0.423,1.068,0.157,1.857,0.077,2.054c0.497,0.542,0.798,1.235,0.798,2.082 c0,2.981-1.814,3.637-3.543,3.829c0.279,0.24,0.527,0.713,0.527,1.437c0,1.037-0.01,1.874-0.01,2.129 c0,0.208,0.14,0.449,0.534,0.373c3.081-1.028,5.302-3.935,5.302-7.362C15.76,3.906,12.285,0.431,7.999,0.431z"/></svg>
</span><span class="username">duplys</span></a>

          </li>
          

          
          <li>
            <a href="https://twitter.com/jekyllrb"><span class="icon icon--twitter"><svg viewBox="0 0 16 16"><path fill="#828282" d="M15.969,3.058c-0.586,0.26-1.217,0.436-1.878,0.515c0.675-0.405,1.194-1.045,1.438-1.809c-0.632,0.375-1.332,0.647-2.076,0.793c-0.596-0.636-1.446-1.033-2.387-1.033c-1.806,0-3.27,1.464-3.27,3.27 c0,0.256,0.029,0.506,0.085,0.745C5.163,5.404,2.753,4.102,1.14,2.124C0.859,2.607,0.698,3.168,0.698,3.767 c0,1.134,0.577,2.135,1.455,2.722C1.616,6.472,1.112,6.325,0.671,6.08c0,0.014,0,0.027,0,0.041c0,1.584,1.127,2.906,2.623,3.206 C3.02,9.402,2.731,9.442,2.433,9.442c-0.211,0-0.416-0.021-0.615-0.059c0.416,1.299,1.624,2.245,3.055,2.271 c-1.119,0.877-2.529,1.4-4.061,1.4c-0.264,0-0.524-0.015-0.78-0.046c1.447,0.928,3.166,1.469,5.013,1.469 c6.015,0,9.304-4.983,9.304-9.304c0-0.142-0.003-0.283-0.009-0.423C14.976,4.29,15.531,3.714,15.969,3.058z"/></svg>
</span><span class="username">jekyllrb</span></a>

          </li>
          
        </ul>
      </div>

      <div class="footer-col footer-col-3">
        <p>Write an awesome description for your new site here. You can edit this line in _config.yml. It will appear in your document head meta (for Google search results) and in your feed.xml site description.
</p>
      </div>
    </div>

  </div>

</footer>


  </body>

</html>
