# Gaining Acceptance from Housemates

A Smart Home brings a lot of benefits when everyone in the household profits from it. Here are tips on how to gain acceptance from your family/housemates.

## Basic Principles

!!!tip "Most Important Rule"
    **Smart Home should make life easier, not more complicated.** If someone can still use a normal light switch, that's a feature, not a bug.

### 1. Start Small

Begin with simple, immediately noticeable improvements:

| Starting Point | Why? |
|----------------|------|
| **Automatic lights** | Lights turn on/off by themselves |
| **Temperature monitoring** | Always the right temperature |
| **Notifications** | "Garage door is open" |
| **Timers** | Coffee machine on in the morning |

### 2. Keep Physical Switches

!!!warning "Don't fear the light switch!"
    Smart devices should ALWAYS be operable manually. A Shelly behind a normal light switch is the perfect solution.

### 3. Simple Operation

| Solution | For whom? |
|----------|-----------|
| **Light switch** | Everyone (always available) |
| **Dashboard on tablet** | Family (overview) |
| **Voice control** | Everyone (convenient) |
| **Automation** | Everyone (invisible) |

## Success Recipes

### The "Magical" Bathroom

```
When: Door is opened
Then: Lights on (dimmed after 10 PM)
When: Motion detected
Then: Lights stay on
When: 5 minutes no motion
Then: Lights off
```

**Reaction:** "Wow, the lights turn on by themselves!"

### The Perfect Morning

```
When: 6:30 AM (weekday)
Then: 
  - Heating to 21°C
  - Coffee machine on
  - Radio softly on
  - Lights slowly brighter (Sunrise)
```

**Reaction:** "The coffee is ready when I get up!"

### The Nice Evening

```
When: Sunset
Then: Outdoor lights on
When: Everyone leaves the house
Then: All lights off, heating down
When: Someone comes home
Then: Hallway light on, heating up
```

## Voice Control

Voice control makes Smart Home accessible to everyone:

### Home Assistant + Assist

With Home Assistant's Assist (local, no cloud):
- "Turn on the living room light"
- "How warm is it outside?"
- "Play music in the bedroom"

### Amazon Alexa / Google Home

Integration via Home Assistant:
- Voice commands for all devices
- No cloud lock-in (Home Assistant remains the central hub)

!!!tip "Consider Privacy"
    For privacy-friendly voice control, use [Home Assistant Assist](https://www.home-assistant.io/voice_control/) with local speech recognition.

## Persuasion Strategies

### For Partners

| Argument | Example |
|----------|---------|
| **Convenience** | "You don't have to get up to turn off the light anymore" |
| **Security** | "We can see if the front door is open" |
| **Savings** | "The heating only runs when someone is home" |
| **Invisibility** | "You don't even notice it, it just works" |

### For Children

| Feature | Why it's cool |
|---------|---------------|
| **Own Dashboard** | "Look, you can control your own light" |
| **"Light Show"** | Colored LED strips |
| **Notifications** | "Package has arrived!" |
| **Voice control** | "Just say 'Good night'" |

### For Skeptical Housemates

1. **Show, don't tell** — Let them experience it for a week
2. **Start with their problem** — "You hate having cold feet? Check this out..."
3. **Stay modest** — Not everything at once
4. **Accept "no"** — Not every room needs to be smart

## Do's and Don'ts

### ✅ Do's

- ✅ Keep physical switches
- ✅ Start with simple automations
- ✅ Prefer local control (no cloud dependency)
- ✅ Use good naming ("Living room light" not "light_1")
- ✅ Have backup plans (what if the server goes down?)
- ✅ Regular updates

### ❌ Don'ts

- ❌ Replace all switches with displays
- ❌ Force complicated workflows
- ❌ Make rooms smart without consent
- ❌ Create cloud dependencies
- ❌ Send too many notifications
- ❌ Do everything at once

## Example Scenarios

### "Smart Home Light" (Beginner)

- 3-5 smart outlets/lamps
- 1 temperature sensor
- Automatic timers
- **Budget:** ~100€

### "Smart Home Plus" (Standard)

- Smart lights in main rooms
- Temperature and humidity sensors
- Door contact front door/garage
- Dashboard on old tablet
- **Budget:** ~300€

### "Full Smart Home" (Advanced)

- All lights smart
- All radiators smart
- Cameras/burglar protection
- Voice control
- Energy monitoring
- **Budget:** ~1000€+

## Conclusion

!!!success "The Best Smart Home Quote"
    "Smart Home is successful when no one thinks about it anymore — it just works."

Start with a problem that needs to be solved. Not with technology that looks cool.

## More Information

- [Edge Devices](../hardware/edge-devices.md) - What devices are available?
- [Home Assistant](../software/homeassistant.md) - The central hub
- [NodeRED](../software/nodered.md) - For complex automations
