timekill
========

[![Build](https://github.com/ErikBjare/timekill/actions/workflows/build.yml/badge.svg)](https://github.com/ErikBjare/timekill/actions/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Typechecking: mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

A better way to kill time.

An app that suggests healthy ways for you to spend your time, in a context-aware way.

> **Note**
> This project is a work-in-progress.

Features:

 - A day-planner that suggests activities for you to do
   - Taking into account context like time, activity type (work, leisure, etc.), and location. 
   - When configured with activities and the conditions for recommending them, can help you sort out what to do with your days.

 - A recommender system for content *that you control*.
   - Gets content from reddit (later Twitter, Hacker News, etc.)
   - Includes WIP/experimental content classification/recommendation based on GPT-3.

## Usage

```
$ timekill --help
Usage: timekill [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  list     List content with recommendations.
  plan     Plan a day of activity.
  start    Entrypoint for the timekill server
  suggest  Suggest activities to do.
```

---

**Note:** the text below was written a long time ago, and does not represent the current state of the project.

## Why?

Most of us are guilty of using our phones too much, which wouldn't be a problem if most of the use was actually healthy. Instead we spend far more time than we should on social media, YouTube, Netflix, and games. What if we could wire our brains to compulsively open an app that suggested [healthy alternatives](#healthy-timekill) instead?

What I suggest is a feed that serves cards with *healthy* and *productive* content. Content feeds are powerful tools that capture our attention by exploiting our brains' desire for novelty. The question is: can we tame it?


## Healthy timekill

Here's a list of healthy ways to kill time:

 - Work on a task on your TODO list
 - Use learning apps like Brilliant/Khan Academy/Coursera/EdX/Duolingo
 - Work out at home or go to the gym
 - Get only the most useful/recommended content across feeds (see my wiki on [The Importance of Open Recommender Systems](https://erik.bjareholt.com/wiki/importance-of-open-recommendation-systems/))
   - Can this actually decrease FOMO meaningfully?
 - Staying in touch with friends we haven't talked to in a while (as some personal relationship management systems aim to help the user do)

The important thing for things to make a list like this is that it's something the user could *sometimes* actually be willing to do. Different times/moods/places call for different timekill.


## Ideas

 - Integrate with ActivityWatch
   - Track how many productive hours timekill helped initiate.
   - Show a card with the number of productive hours today
     - You could do the same for unproductive hours, but I'm not sure that would be very helpful as it basically just shames the user (which could lead to counterproductive results)
 - Add rewards for productive time (this might be a bad idea, would make the motivation extrinsic)
 - Distraction-distracting notifications: Try to distract the user from undesirable activities (social media, games, etc.) by sending notifications that suggest healthier alternatives

## Timeline

### Pre-MVP

 - [x] Build a CLI-version of the app (for quick iteration on new features)
 - [ ] Build a very basic web frontend? (for quick GUI iteration)

### MVP

How do we build an MVP that users like and find helpful as quickly as possible?

 - [ ] Needs a way to configure your own activities
   - How do we get the user to think about good ways to kill time? Offer suggestions/good defaults?
 - [ ] Make it usable from phone
 - [ ] (optional) Integrate with ActivityWatch for better context-awareness

### Marketing

 - Set up a ProductHunt ship page (to build a mailing list of people who are interested)
   - Link from personal, ActivityWatch, and Thankful accounts on social media
   - Share in local college/programming/startup communities (Code@LTH, D-sektionen community, Lund Startups, Malmö Startups)


## Name

Current name was just how the one I happened to impulsively use when thinking about it. It might need improvement.

## Similar software

I've discovered similar software that does part of what timekill does.

Automatic scheduling:
 - Google Calendar's "Goals" feature
 - https://usemotion.com/
 - https://super-productivity.com/ (maybe? Haven't used)

Self-hosted/open-source/personal recommender system:
 - None?
