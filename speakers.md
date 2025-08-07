---
layout: page
title: Keynote Speakers
permalink: /speakers/
---

Our symposium features distinguished interventional radiologists and MRI specialists from prestigious institutions worldwide who will share their expertise and insights on advanced MRI-guided interventions.

{% for speaker in site.speakers %}
<div class="speaker-card">
  <h2><a href="{{ speaker.url | relative_url }}">{{ speaker.title }}</a></h2>
  <h3>{{ speaker.position }}, {{ speaker.institution }}</h3>
  <p><strong>Talk: </strong>{{ speaker.talk_title }}</p>
  <p>{{ speaker.bio | truncate: 150 }}</p>
  <a href="{{ speaker.url | relative_url }}" class="read-more">Read more</a>
</div>
{% endfor %}

## Call for Speakers

We are currently finalizing our speaker lineup. If you are interested in giving a keynote or invited talk at the 15th Interventional MRI Symposium, please contact our program committee at [program@example.org](mailto:program@example.org).

**Note:** Current speaker profiles are placeholders and will be updated with confirmed speakers as they are announced.
