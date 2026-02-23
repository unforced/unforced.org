---
title: "Building in the Margins"
subtitle: "On weekend projects, free software, and who we build for"
date: 2025-12-23
author: "Aaron G Neyer"
source: "https://unforced.substack.com/p/building-in-the-margins"
tags: []
---

![](/images/posts/building-in-the-margins-1.png)
A few weeks ago, I hopped on a call with someone I’d just been introduced to. We quickly found a lot of overlap in how we were looking at things. He started describing a project he was working on — something that would pull together people’s astrology charts, Human Design profiles, and Gene Keys, then use all that data to calculate compatibility for collaboration.

I smiled. Once upon a time, I’d had a similar idea. I told him I’d actually started building something like this years ago but never followed through. “But now,” I said, “with AI being what it is, this whole thing could pretty much be a weekend project.”

He was surprised. So I walked him through how I’d prompt it — the vision, the architecture, the sequence. And then, while we were still on the call, I pulled the transcript from my AI notetaker, copied it, and pasted it directly into Claude.

A bit of back and forth that night and the next morning, and I had a working MVP. By the end of the weekend, I had NatalEngine.

---

### The Itch

Here’s the funny thing: I’m less into these systems than I used to be. Astrology, Human Design, Gene Keys — I went through a phase where I was deep in all of it. These days, I’m more skeptical of their value, though I still find them interesting.

But a lot of my friends are still really into these systems. And if something is meaningful to people I care about, that’s reason enough to build.

There’s something clarifying about building for people you actually know. You’re not guessing at market fit or chasing some abstract user persona. You’re just making something useful for your friends and seeing what happens.

---

### What I Built

NatalEngine is an open source JavaScript library that calculates birth charts for three systems: Western Astrology, Human Design, and Gene Keys. It returns clean, structured data — no interpretations, just the facts. The idea is that the interpretation layer can live somewhere else (like in a conversation with an AI that knows you).

Because it’s a library, other developers can easily incorporate these systems into their own apps. And because I built an MCP server for it, you can integrate it directly into Claude or other AI systems — just ask for your chart in conversation and it pulls the data. (And if “MCP server” is a foreign concept to you, keep an eye out for [Parachute](https://openparachute.substack.com/) — I’m hoping to make a lot of these fancy AI things more simple and accessible.) There’s also a simple website where you can punch in your birth info and get your charts directly.

It’s all open source if you want to poke around: [natalengine.com](https://natalengine.com/)

---

### The Paradigm

I keep coming back to what this means about how we build now.

A few months ago, I wrote about this shift in [Building with Words](https://unforced.substack.com/p/building-with-words) — how the tools are changing, how articulation is becoming the core skill, how my dialogue-loving side and my builder side are finally merging. NatalEngine is another data point in that story.

This was an idea I’d carried for years. On a call with someone working on something similar, I realized the moment had arrived. I described how I’d build it, copied that description into my AI system, and by the end of the weekend I had a polished, working product.

Not working full-time on it, either. I was fitting it between other activities, even building it alongside other projects. The weekend wasn’t consumed by this — it just happened, almost as a side effect of having the right conversation at the right time.

That’s the shift. Ideas that once required months of focused effort can now be built in days, in the margins.

---

### Software as Public Good

This changes what software can be.

If something can be built, it can be rebuilt. And if it can be rebuilt fast, there’s less reason for simple tools to cost money.

I’ve been thinking a lot about this. There are so many apps out there that cost $5 or show a bunch of ads — little utilities that do one thing reasonably well. I want to start rebuilding some of those. Free. Open source. No tracking, no subscription, no bullshit.

In fact, this same weekend, while building NatalEngine, I was also working on another project — a collection of simple phone utilities that you often have to sit through ads or pay money for. I’ll share more on that soon, but the point is: I was building multiple projects simultaneously, fitting them between other activities. That’s the shift.

And I was also building [Parachute](http://openparachute.io/) that same weekend — a personal knowledge management system I’ve been developing. The same patterns and components going into Parachute are what enabled me to move efficiently between these projects. I’ll share more about it soon.

In my ideal world, good simple tools are just accessible to people. Technology is a public good. I recognize this might bother some indie developers who rely on the $5 from that little app they made. But I think it’s more important to give people good tooling. And honestly, in a world where building is this fast, the defensibility of simple software was always going to erode. Better to lean into that and build for the commons.

NatalEngine is a small example of this. Most astrology, Human Design, and Gene Keys apps will give you the basic readings for free — but they want your email, and they’re trying to sell you something later. NatalEngine doesn’t want anything from you. It’s free, it’s open, and anyone can use it, fork it, or build on it.

---

### Building for People You Know

The thing that excites me most about this project isn’t the tech. It’s that my friends will actually use it.

I’m orienting more and more around this. Building for people I know. People who will actually give me feedback. People I’m in relationship with. This creates a different kind of loop — not metrics and analytics, but conversations and trust.

I’ve already started setting up time with friends who are really into these systems. There’s a good chance NatalEngine will evolve significantly over the coming weeks just from those conversations — good feedback and ideas from the people I’m actually building for. And because of how fast building is now, I can incorporate that feedback directly into the app almost as quickly as I hear it.

When you build for your community, you start to become someone they see as able to meet their technology needs. That’s a role I want to grow into. Not as a service provider, but as a friend who builds things.

I’m curious what resonates here. Is this kind of tool useful to you? Are there other things you wish existed but don’t — or exist but feel extractive? I’m genuinely interested in what people need, especially people I actually know.

We’re entering an era where building is fast and cheap. I want to point that capacity toward things that matter.

---

*If you want to try NatalEngine, the calculator is at [natalengine.com](https://natalengine.com/) and the code is on [GitHub](https://github.com/unforced-dev/natal-engine).*

*And yes, this article was written with AI. Here's an AI-generated song to go with it:*