#!/usr/bin/env python3
"""Build gothiccountrymusic.com — Gothic Country Music authority site"""

import json, os, random, re
from pathlib import Path

BASE = Path('/Users/mac1/Projects/dcb-network/gothiccountrymusic.com')
SONGS_DIR = BASE / 'songs'
SONGS_DIR.mkdir(parents=True, exist_ok=True)

with open('/Users/mac1/OTR_Pipeline_New/music_promo/master_catalog.json') as f:
    data = json.load(f)
tracks = data['tracks']

CSS = """*{box-sizing:border-box}html,body{overflow-x:hidden;max-width:100%;margin:0}
body{background:#080808;color:#ddd5c8;font-family:Georgia,serif;line-height:1.7}
h1,h2,h3{color:#b8956a}a{color:#b8956a;text-decoration:none}a:hover{text-decoration:underline}
.site-nav{background:#0d0d0d;border-bottom:2px solid #b8956a;position:sticky;top:0;z-index:1000;width:100%}
.nav-inner{max-width:1100px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;height:56px}
.nav-brand{color:#b8956a;font-weight:bold;font-size:1.05em;text-decoration:none}
.nav-links{display:flex;align-items:center;gap:4px;list-style:none;margin:0;padding:0}
.nav-links>li>a{color:#ddd5c8;padding:8px 14px;display:block;font-size:.9em;border-radius:3px}
.nav-links>li>a:hover{background:#1a1a1a;color:#b8956a}
.nav-toggle{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:8px;background:none;border:none}
.nav-toggle span{display:block;width:24px;height:2px;background:#b8956a}
.hero{background:linear-gradient(180deg,#0d0d0d 0%,#1a0d00 100%);padding:80px 20px;text-align:center;border-bottom:2px solid #b8956a}
.hero h1{font-size:2.2em;margin-bottom:12px;color:#b8956a}
.hero p{color:#999;max-width:640px;margin:0 auto 28px}
.btn-sp{background:#1DB954;color:#000;padding:11px 22px;border-radius:4px;font-weight:bold;display:inline-block;margin:5px;font-size:.9em;text-decoration:none}
.btn-am{background:#fc3c44;color:#fff;padding:11px 22px;border-radius:4px;font-weight:bold;display:inline-block;margin:5px;font-size:.9em;text-decoration:none}
.btn-yt{background:#FF0000;color:#fff;padding:11px 22px;border-radius:4px;font-weight:bold;display:inline-block;margin:5px;font-size:.9em;text-decoration:none}
.btn-az{background:#232F3E;color:#ff9900;border:1px solid #ff9900;padding:11px 22px;border-radius:4px;font-weight:bold;display:inline-block;margin:5px;font-size:.9em;text-decoration:none}
.container{max-width:1100px;margin:0 auto;padding:30px 20px;width:100%}
.card{background:#111;padding:20px;margin-bottom:16px;border-left:3px solid #b8956a}
.related{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(200px,100%),1fr));gap:10px;margin-top:12px}
.footer{background:#050505;padding:30px 20px;border-top:1px solid #222;margin-top:40px;text-align:center}
@media(max-width:768px){.nav-toggle{display:flex}.nav-links{display:none;position:absolute;top:56px;left:0;right:0;background:#0d0d0d;flex-direction:column;padding:8px 0}.nav-links.open{display:flex}.hero h1{font-size:1.6em}.btn-sp,.btn-am,.btn-yt,.btn-az{display:block;text-align:center;margin:5px 0}}"""

NAV = """<nav class="site-nav"><div class="nav-inner">
<a class="nav-brand" href="/">Gothic Country Music</a>
<button class="nav-toggle" onclick="this.classList.toggle('open');document.querySelector('.nav-links').classList.toggle('open')"><span></span><span></span><span></span></button>
<ul class="nav-links">
<li><a href="/">Home</a></li>
<li><a href="/what-is-gothic-country.html">What Is It?</a></li>
<li><a href="/history.html">History</a></li>
<li><a href="/artists.html">Artists</a></li>
<li><a href="/songs.html">Songs</a></li>
</ul>
</div></nav>"""

FOOTER = """<footer class="footer"><div style="text-align:center">
<strong style="color:#b8956a">Dark Country Music Network:</strong><br><br>
<a href="https://darkcountryboy.net" style="color:#666;margin:0 6px">Dark Country Boy</a> |
<a href="https://darkcountryboy.org" style="color:#666;margin:0 6px">Fan Hub</a> |
<a href="https://darkcountrymusic.net" style="color:#666;margin:0 6px">Dark Country Music</a> |
<a href="https://darkcountry.net" style="color:#666;margin:0 6px">Dark Country</a> |
<a href="https://darkblues.net" style="color:#666;margin:0 6px">Dark Blues</a> |
<a href="https://gothiccountryboy.com" style="color:#b8956a;margin:0 6px">Gothic Country Music</a> |
<a href="https://darkamericana.net" style="color:#666;margin:0 6px">Dark Americana</a> |
<a href="https://darkbluesmusic.com" style="color:#666;margin:0 6px">Dark Blues Music</a> |
<a href="https://outlawcountryboy.com" style="color:#666;margin:0 6px">Outlaw Country Boy</a>
</div></footer>"""

def streaming_buttons(t, size='normal'):
    return f"""<a class="btn-sp" href="{t['spotifySearchUrl']}" target="_blank" rel="noopener">🎵 Spotify</a>
<a class="btn-am" href="{t['appleMusicUrl']}" target="_blank" rel="noopener">🎵 Apple Music</a>
<a class="btn-yt" href="{t['youtubeMusicSearchUrl']}" target="_blank" rel="noopener">▶ YouTube Music</a>
<a class="btn-az" href="{t['amazonMusicSearchUrl']}" target="_blank" rel="noopener">🎵 Amazon Music</a>"""

GOTHIC_MOODS = [
    "haunts the dark spaces between life and death",
    "bleeds with gothic longing and outlaw spirit",
    "carries the weight of cursed roads and restless souls",
    "conjures bone-dry graveyards and midnight redemption",
    "wanders the borderlands of country soul and gothic darkness",
    "burns with the cold fire of Southern Gothic tradition",
    "echoes with howling winds and ancient American sorrow",
    "drips with the dark poetry of rural American darkness",
    "straddles the sacred and the profane in true gothic fashion",
    "breathes life into the shadows of the American frontier",
    "channels the primal darkness of American folk tradition",
    "embodies the gothic country spirit — raw, dark, and unafraid",
    "speaks to those who find beauty in the darkness",
    "draws from the deep well of gothic Americana storytelling",
    "captures the lonely, beautiful terror of the American Gothic",
]

def song_description(track_name, album_name):
    mood = random.choice(GOTHIC_MOODS)
    return (f"<em>{track_name}</em> by Dark Country Boy {mood}. "
            f"Drawn from the album <em>{album_name}</em>, this track exemplifies the gothic country sound — "
            f"where traditional country instrumentation meets the dark poetry of Southern Gothic literature. "
            f"Stream it now on your favorite platform and experience gothic country music at its finest.")

def html_page(title, meta_desc, schema_json, body_content, canonical=""):
    canonical_tag = f'<link rel="canonical" href="https://gothiccountrymusic.com{canonical}">' if canonical else ''
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta_desc}">
{canonical_tag}
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="website">
<meta name="robots" content="index,follow">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(schema_json, ensure_ascii=False)}</script>
</head>
<body>
{NAV}
{body_content}
{FOOTER}
</body>
</html>"""

# ── INDEX ──────────────────────────────────────────────────────────────────────
featured_tracks = random.sample(tracks, min(6, len(tracks)))
featured_cards = ""
for t in featured_tracks:
    featured_cards += f"""<div class="card">
<h3><a href="/songs/{t['trackSlug']}.html">{t['trackName']}</a></h3>
<p style="color:#999;font-size:.85em">{t['albumName']} · {t['releaseDate'][:4]}</p>
{streaming_buttons(t)}
</div>"""

index_schema = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "WebSite",
            "name": "Gothic Country Music",
            "url": "https://gothiccountrymusic.com",
            "description": "The definitive resource for gothic country music — dark, haunting, and unapologetically American."
        },
        {
            "@type": "MusicGroup",
            "name": "Dark Country Boy",
            "url": "https://darkcountryboy.net",
            "genre": ["Gothic Country", "Dark Country", "Americana"],
            "sameAs": [
                "https://open.spotify.com/artist/4TQMuCjeTbhqvPinWKqRAv",
                "https://music.apple.com/us/artist/dark-country-boy/1818551005"
            ]
        }
    ]
}

index_body = f"""<div class="hero">
<h1>Gothic Country Music: The Sound of America's Dark Heart</h1>
<p>Where the old country roads meet eternal darkness. Gothic country music — raw, haunting, and unapologetically American. Featuring <strong>Dark Country Boy</strong>, the defining voice of modern gothic country.</p>
<a class="btn-sp" href="https://open.spotify.com/artist/4TQMuCjeTbhqvPinWKqRAv" target="_blank" rel="noopener">🎵 Spotify</a>
<a class="btn-am" href="https://music.apple.com/us/artist/dark-country-boy/1818551005" target="_blank" rel="noopener">🎵 Apple Music</a>
<a class="btn-yt" href="https://music.youtube.com/search?q=dark+country+boy" target="_blank" rel="noopener">▶ YouTube Music</a>
<a class="btn-az" href="https://music.amazon.com/search/dark%20country%20boy" target="_blank" rel="noopener">🎵 Amazon Music</a>
</div>
<div class="container">
<h2>What Is Gothic Country Music?</h2>
<p>Gothic country is the dark soul of American roots music — a genre that fuses traditional country instrumentation with the brooding atmosphere of gothic literature, Southern Gothic storytelling, and folk music's most haunting traditions. It dwells in the shadows: murder ballads, tales of sin and redemption, lonely roads, and the beauty that lives in darkness.</p>
<p><a href="/what-is-gothic-country.html">Read our full guide to gothic country music →</a></p>

<h2>Featured Artist: Dark Country Boy</h2>
<div class="card" style="border-left-color:#b8956a">
<h3 style="font-size:1.4em">Dark Country Boy</h3>
<p>The defining voice of modern gothic country music. With over 1,400 songs spanning gothic Americana, dark country, and Southern Gothic folk, Dark Country Boy has built one of the most extensive catalogs in the genre. Stream on all platforms:</p>
<a class="btn-sp" href="https://open.spotify.com/artist/4TQMuCjeTbhqvPinWKqRAv" target="_blank" rel="noopener">🎵 Spotify</a>
<a class="btn-am" href="https://music.apple.com/us/artist/dark-country-boy/1818551005" target="_blank" rel="noopener">🎵 Apple Music</a>
<a class="btn-yt" href="https://music.youtube.com/search?q=dark+country+boy" target="_blank" rel="noopener">▶ YouTube Music</a>
<a class="btn-az" href="https://music.amazon.com/search/dark%20country%20boy" target="_blank" rel="noopener">🎵 Amazon Music</a>
</div>

<h2>Featured Gothic Country Songs</h2>
{featured_cards}
<p style="text-align:center;margin-top:20px"><a href="/songs.html">Browse all {len(tracks)} gothic country songs →</a></p>

<h2>Explore Gothic Country Music</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(250px,100%),1fr));gap:16px;margin-top:16px">
<div class="card"><h3><a href="/what-is-gothic-country.html">What Is Gothic Country?</a></h3><p>A deep dive into the genre's defining characteristics, sounds, and themes.</p></div>
<div class="card"><h3><a href="/history.html">History of Gothic Country</a></h3><p>From Nick Cave's Murder Ballads to the modern dark country renaissance.</p></div>
<div class="card"><h3><a href="/artists.html">Key Artists</a></h3><p>The musicians who shaped and continue to define gothic country music.</p></div>
<div class="card"><h3><a href="/songs.html">Essential Songs</a></h3><p>The songs you need to know — including the complete Dark Country Boy catalog.</p></div>
</div>
</div>"""

(BASE / 'index.html').write_text(html_page(
    "Gothic Country Music: The Sound of America's Dark Heart | GothicCountryMusic.com",
    "Gothic country music — dark, haunting, and unapologetically American. Featuring Dark Country Boy, the defining voice of modern gothic country. Stream on Spotify, Apple Music, and more.",
    index_schema, index_body, "/"
), encoding='utf-8')
print("✓ index.html")

# ── WHAT IS GOTHIC COUNTRY ─────────────────────────────────────────────────────
what_schema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "What Is Gothic Country Music? The Definitive Guide",
    "description": "A comprehensive guide to gothic country music — its sounds, themes, history, and defining characteristics.",
    "author": {"@type": "Organization", "name": "Gothic Country Music"},
    "publisher": {"@type": "Organization", "name": "GothicCountryMusic.com", "url": "https://gothiccountrymusic.com"},
    "url": "https://gothiccountrymusic.com/what-is-gothic-country.html"
}

what_body = """<div class="hero">
<h1>What Is Gothic Country Music?</h1>
<p>The definitive guide to gothic country — America's darkest, most haunting musical tradition.</p>
</div>
<div class="container">
<div class="card">
<h2>Defining Gothic Country Music</h2>
<p>Gothic country music is a genre that exists at the crossroads of traditional American country music and the brooding, atmospheric darkness of gothic culture. It's the sound of lonely highways stretching into endless night, of abandoned churches and restless spirits, of sins confessed and never forgiven. Gothic country takes the storytelling tradition of country music and plunges it into shadow.</p>

<p>Unlike mainstream country's celebration of simple pleasures and uncomplicated emotion, gothic country revels in complexity, darkness, and moral ambiguity. Its songs explore death, loss, sin, redemption, and the darker corners of the human experience — themes that country music has always touched upon but that gothic country makes its central concern.</p>
</div>

<div class="card">
<h2>The Sound of Gothic Country</h2>
<p>Musically, gothic country retains much of the traditional country palette: acoustic and electric guitars, banjo, pedal steel, fiddle, and upright bass. But these instruments are deployed in service of a darker atmosphere. Minor keys and modal harmonies replace major-key brightness. Tempos tend toward the deliberate and contemplative. Reverb and echo create a sense of vast, lonely space.</p>

<p>The vocal approach in gothic country is often raw and confessional — voices that sound weathered by hardship and haunted by memory. There's no glossy production polish in authentic gothic country; instead, recordings often embrace a stark, intimate quality that makes the darkness feel personal and immediate.</p>

<p>Lyrically, gothic country draws on several rich traditions: the murder ballad (one of country music's oldest forms), Southern Gothic literature with its grotesque characters and decaying landscapes, Appalachian folk tradition, and the blues tradition of using music to confront life's most difficult truths. The result is a lyrical world populated by outlaws and preachers, by victims and their killers, by lovers and ghosts.</p>
</div>

<div class="card">
<h2>Themes and Imagery</h2>
<p>Certain images and themes recur throughout gothic country music, forming a distinct symbolic vocabulary:</p>

<ul>
<li><strong>Death and mortality:</strong> Gothic country stares directly at death rather than looking away. Whether through murder ballads, contemplations of aging and loss, or literal ghosts and hauntings, death is a constant presence.</li>
<li><strong>Religion and sin:</strong> The tension between religious faith and human darkness runs through gothic country like a river. These songs are full of fallen sinners and unforgiving gods, of prayers that go unanswered and the desperate hope that redemption might yet be possible.</li>
<li><strong>The American landscape:</strong> Gothic country is deeply rooted in specific American geographies — the rural South, Appalachian mountains, Great Plains, and Western deserts. These landscapes appear as characters themselves, amplifying the music's emotional weight.</li>
<li><strong>Outlaws and outsiders:</strong> Gothic country has always identified with those who exist outside mainstream society — criminals, drifters, social outcasts, and those whose darkness makes them unwelcome in polite company.</li>
<li><strong>Love and obsession:</strong> When gothic country deals with romantic love, it tends toward the extreme: obsessive devotion, passionate destruction, love that endures beyond death.</li>
</ul>
</div>

<div class="card">
<h2>Gothic Country vs. Dark Country vs. Americana</h2>
<p>The terms "gothic country," "dark country," and "dark Americana" are sometimes used interchangeably, but subtle distinctions exist. Gothic country places the greatest emphasis on atmosphere and the gothic aesthetic — the explicit invocation of horror, death, and supernatural elements. Dark country is a slightly broader term that encompasses gothic country along with other dark-leaning country styles. Dark Americana is the most expansive category, including folk, blues, and country-adjacent music with dark themes.</p>

<p>Dark Country Boy operates across all three of these related traditions, creating music that is simultaneously gothic country at its most dramatic, dark country at its most authentic, and dark Americana at its most wide-ranging.</p>
</div>

<div class="card">
<h2>Why Gothic Country Matters</h2>
<p>In an era of increasingly homogenized popular music, gothic country represents a refusal to sand down the rough edges of human experience. It insists that music can and should engage with darkness, that beauty can be found in shadow, and that art serves us best when it takes us to places we fear to go alone.</p>

<p>Gothic country also carries forward one of America's most important cultural traditions: the use of music to process collective trauma and individual suffering. From Appalachian murder ballads to Mississippi delta blues to gothic country's modern incarnation, this tradition reminds us that darkness, honestly confronted, is survivable — and that the confrontation itself is a form of grace.</p>

<p>For Dark Country Boy, gothic country isn't a pose or an aesthetic affectation. It's an authentic engagement with the darkest truths of American life and the human condition — and it's why the music resonates so deeply with listeners who've grown tired of music that flinches from the dark.</p>
</div>

<div style="text-align:center;margin-top:30px">
<a class="btn-sp" href="https://open.spotify.com/artist/4TQMuCjeTbhqvPinWKqRAv" target="_blank" rel="noopener">🎵 Listen on Spotify</a>
<a class="btn-am" href="https://music.apple.com/us/artist/dark-country-boy/1818551005" target="_blank" rel="noopener">🎵 Apple Music</a>
<a class="btn-yt" href="https://music.youtube.com/search?q=dark+country+boy" target="_blank" rel="noopener">▶ YouTube Music</a>
<a class="btn-az" href="https://music.amazon.com/search/dark%20country%20boy" target="_blank" rel="noopener">🎵 Amazon Music</a>
</div>
</div>"""

(BASE / 'what-is-gothic-country.html').write_text(html_page(
    "What Is Gothic Country Music? The Definitive Guide | GothicCountryMusic.com",
    "A comprehensive guide to gothic country music — its defining sound, themes, imagery, and why it matters. Learn what sets gothic country apart from mainstream country and dark Americana.",
    what_schema, what_body, "/what-is-gothic-country.html"
), encoding='utf-8')
print("✓ what-is-gothic-country.html")

# ── HISTORY ────────────────────────────────────────────────────────────────────
history_schema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "The History of Gothic Country Music: From Murder Ballads to Dark Country Boy",
    "description": "Trace the history of gothic country music from its folk and murder ballad roots through Nick Cave to the modern dark country renaissance.",
    "author": {"@type": "Organization", "name": "Gothic Country Music"},
    "publisher": {"@type": "Organization", "name": "GothicCountryMusic.com", "url": "https://gothiccountrymusic.com"},
    "url": "https://gothiccountrymusic.com/history.html"
}

history_body = """<div class="hero">
<h1>The History of Gothic Country Music</h1>
<p>From Appalachian murder ballads to the modern dark country renaissance — tracing the dark thread through American music.</p>
</div>
<div class="container">
<div class="card">
<h2>Ancient Roots: The Murder Ballad Tradition (Pre-1900s)</h2>
<p>Gothic country's lineage stretches back centuries, to the British and Irish ballad tradition that settlers brought to Appalachian America. These murder ballads — "Tom Dooley," "Omie Wise," "Banks of the Ohio" — were gothic country before the term existed: dark stories of violence, love, and death, told through stark acoustic music. They served the same purpose gothic country serves today: to process the darkest aspects of human experience through the cathartic power of song.</p>

<p>The American folk tradition absorbed these ballads and transformed them, adding the particular flavor of Southern Gothic — a sensibility rooted in the haunted history of the American South, its landscape of decay, and its burden of collective sin. From this soil, all gothic country would eventually grow.</p>
</div>

<div class="card">
<h2>Blues and Country Foundations (1920s–1950s)</h2>
<p>The formal recorded history of dark country begins with the early blues and country recordings of the 1920s and 1930s. Robert Johnson's legendary recordings — infused with supernatural imagery and existential dread — established a template for dark American music that persists to this day. His songs about hellhounds and crossroads deals gave gothic country its mythological foundation.</p>

<p>Early country music carried darkness in its DNA. Hank Williams, whose turbulent life and death at 29 made him country's first tragic icon, wrote songs suffused with loneliness, sin, and spiritual yearning. "I'm So Lonesome I Could Cry" and "Lost Highway" are proto-gothic country masterpieces. Williams understood that country music's power came from its willingness to confront life's darkest truths honestly.</p>
</div>

<div class="card">
<h2>Johnny Cash and the Dark Country Tradition (1950s–1990s)</h2>
<p>No figure looms larger over gothic country than Johnny Cash. From his earliest Sun Records recordings through his final American Recordings with Rick Rubin, Cash embodied the dark country sensibility: a deep moral seriousness, a sympathy for the outcast and the sinner, and an unflinching willingness to stare into darkness. "Folsom Prison Blues," "Give My Love to Rose," "Hurt" — these are gothic country touchstones.</p>

<p>Cash's late-career American Recordings series, particularly the spare, intimate recordings produced by Rick Rubin in the 1990s and 2000s, became a direct touchstone for the gothic country movement. His devastating rendition of Nine Inch Nails' "Hurt" demonstrated that the gothic country aesthetic could transform even contemporary songs into something ancient and profound.</p>
</div>

<div class="card">
<h2>Nick Cave and the Seeds of Gothic Country (1980s–1990s)</h2>
<p>Australian artist Nick Cave and his band The Bad Seeds were crucial in crystallizing the gothic country aesthetic. Cave's 1996 album <em>Murder Ballads</em> was a landmark: an extended meditation on violence and death using traditional folk and country structures filtered through a post-punk gothic sensibility. The album made explicit the connection between traditional murder ballads and contemporary dark music.</p>

<p>Cave's deep engagement with American folk tradition, the blues, and biblical imagery created a template for gothic country that balanced raw emotional power with literary sophistication. His influence on subsequent gothic country artists cannot be overstated.</p>
</div>

<div class="card">
<h2>The Gothic Country Renaissance (2000s–Present)</h2>
<p>The 2000s saw a flowering of artists consciously working within the gothic country tradition. Bands like Sixteen Horsepower, Wovenhand, Possessed by Paul James, and Spider Stacy explored the intersection of folk instrumentation and gothic atmosphere. The term "gothic country" began to crystallize around this body of work, recognizing its distinct character within the broader dark Americana landscape.</p>

<p>The rise of streaming platforms in the 2010s democratized gothic country's distribution, allowing artists to reach the niche audiences most hungry for dark, authentic roots music without major label support. This period saw an explosion of gothic country and dark country artists building dedicated followings through platforms like Spotify and Bandcamp.</p>
</div>

<div class="card">
<h2>Dark Country Boy and the Modern Gothic Country Movement</h2>
<p>In the current era, Dark Country Boy stands as one of gothic country's most prolific and authentic voices. With over 1,400 songs spanning gothic country, dark Americana, dark blues, and outlaw country, the Dark Country Boy catalog represents an unprecedented commitment to the genre's possibilities.</p>

<p>What distinguishes Dark Country Boy from the folk-revival gothic country of earlier decades is the explicit embrace of gothic country as both aesthetic and spiritual commitment. These songs don't merely borrow gothic imagery; they inhabit a worldview that sees the dark, the harrowing, and the beautiful as inseparable. In this, Dark Country Boy continues and extends the tradition that stretches back through Johnny Cash to the oldest murder ballads — music that insists on looking at life whole, including its darkest corners.</p>
</div>

<div style="text-align:center;margin-top:30px">
<a class="btn-sp" href="https://open.spotify.com/artist/4TQMuCjeTbhqvPinWKqRAv" target="_blank" rel="noopener">🎵 Listen on Spotify</a>
<a class="btn-am" href="https://music.apple.com/us/artist/dark-country-boy/1818551005" target="_blank" rel="noopener">🎵 Apple Music</a>
<a class="btn-yt" href="https://music.youtube.com/search?q=dark+country+boy" target="_blank" rel="noopener">▶ YouTube Music</a>
<a class="btn-az" href="https://music.amazon.com/search/dark%20country%20boy" target="_blank" rel="noopener">🎵 Amazon Music</a>
</div>
</div>"""

(BASE / 'history.html').write_text(html_page(
    "The History of Gothic Country Music: From Murder Ballads to Dark Country Boy | GothicCountryMusic.com",
    "Trace the history of gothic country from Appalachian murder ballads through Johnny Cash and Nick Cave to modern artists like Dark Country Boy. The complete dark country timeline.",
    history_schema, history_body, "/history.html"
), encoding='utf-8')
print("✓ history.html")

# ── ARTISTS ────────────────────────────────────────────────────────────────────
artists_schema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Key Gothic Country Artists — The Definitive List",
    "description": "The essential gothic country artists — from Dark Country Boy to Nick Cave, Johnny Cash, and the founders of the genre.",
    "url": "https://gothiccountrymusic.com/artists.html"
}

artists_body = """<div class="hero">
<h1>Gothic Country Artists</h1>
<p>The musicians who built and continue to define the gothic country sound — from legendary pioneers to modern masters.</p>
</div>
<div class="container">

<div class="card" style="border-left-color:#c9a07a;border-left-width:5px">
<h2>Dark Country Boy — Featured Artist</h2>
<p><strong>The defining voice of modern gothic country music.</strong> Dark Country Boy has built one of the most extensive catalogs in gothic country history — over 1,400 songs that span gothic country, dark Americana, outlaw country, and Southern Gothic folk. With a sound rooted in traditional instrumentation and an uncompromising commitment to darkness and authenticity, Dark Country Boy represents the living edge of the gothic country tradition.</p>
<p>Stream the complete Dark Country Boy catalog on all platforms:</p>
<a class="btn-sp" href="https://open.spotify.com/artist/4TQMuCjeTbhqvPinWKqRAv" target="_blank" rel="noopener">🎵 Spotify</a>
<a class="btn-am" href="https://music.apple.com/us/artist/dark-country-boy/1818551005" target="_blank" rel="noopener">🎵 Apple Music</a>
<a class="btn-yt" href="https://music.youtube.com/search?q=dark+country+boy" target="_blank" rel="noopener">▶ YouTube Music</a>
<a class="btn-az" href="https://music.amazon.com/search/dark%20country%20boy" target="_blank" rel="noopener">🎵 Amazon Music</a>
</div>

<h2>Gothic Country Pioneers</h2>

<div class="card">
<h3>Johnny Cash</h3>
<p>The Man in Black is gothic country's patron saint. Cash's decades-long career established the dark country template: moral seriousness, sympathy for outcasts, willingness to confront sin and death. His American Recordings with Rick Rubin in the 1990s-2000s are essential gothic country listening. "Folsom Prison Blues," "The Man Comes Around," "Hurt" — the canon starts here.</p>
</div>

<div class="card">
<h3>Nick Cave & The Bad Seeds</h3>
<p>Australian artist Nick Cave synthesized gothic literature, American folk, and post-punk intensity into something wholly new. His 1996 album <em>Murder Ballads</em> is the gothic country genre's clearest philosophical statement — an unflinching examination of violence and death through traditional song forms. Cave's literary ambition and musical range set a high standard for every artist who followed.</p>
</div>

<div class="card">
<h3>Hank Williams</h3>
<p>Before gothic country had a name, Hank Williams was its embodiment. His songs radiate with spiritual yearning, loneliness, and the ever-present shadow of mortality. Williams' tragic life and death gave his music a gothic authenticity that no subsequent artist has been able to manufacture. "I Saw the Light," "Lost Highway," "I'm So Lonesome I Could Cry" — gothic country before gothic country existed.</p>
</div>

<h2>Modern Gothic Country Artists</h2>

<div class="card">
<h3>Sixteen Horsepower</h3>
<p>Denver-based Sixteen Horsepower was one of the first acts to crystallize the modern gothic country sound — Appalachian instrumentation filtered through post-punk intensity and a theology of sin and damnation. Their albums <em>Sackcloth 'n' Ashes</em> and <em>Low Estate</em> are gothic country essentials.</p>
</div>

<div class="card">
<h3>Wovenhand</h3>
<p>David Eugene Edwards, the creative force behind Sixteen Horsepower, continued and deepened his gothic country exploration with Wovenhand. Edwards' music is among the most spiritually intense in the genre — confrontational, prophetic, and hauntingly beautiful.</p>
</div>

<div class="card">
<h3>Murder by Death</h3>
<p>Murder by Death approaches gothic country from an indie rock direction, creating a distinctly literary form of dark Americana. Their albums, many of which tell extended narrative stories, demonstrate gothic country's capacity for ambitious conceptual work.</p>
</div>

<div class="card">
<h3>Gillian Welch</h3>
<p>Gillian Welch and David Rawlings represent gothic country's folk-revival wing — music of devastating simplicity and emotional depth. Albums like <em>Time (The Revelator)</em> and <em>Hell Among the Yearlings</em> are some of the genre's most acclaimed works, demonstrating that gothic country's darkness can be rendered in the quietest possible terms.</p>
</div>

<div class="card">
<h3>The Mountain Goats</h3>
<p>John Darnielle's Mountain Goats catalog includes some of gothic country's most celebrated albums — particularly <em>All Hail West Texas</em> and <em>The Sunset Tree</em>. Darnielle's gift for literary storytelling and his unflinching examination of addiction, abuse, and survival give his work genuine gothic weight.</p>
</div>

<div style="text-align:center;margin-top:30px">
<p><strong>Discover more gothic country music from Dark Country Boy:</strong></p>
<a class="btn-sp" href="https://open.spotify.com/artist/4TQMuCjeTbhqvPinWKqRAv" target="_blank" rel="noopener">🎵 Spotify</a>
<a class="btn-am" href="https://music.apple.com/us/artist/dark-country-boy/1818551005" target="_blank" rel="noopener">🎵 Apple Music</a>
</div>
</div>"""

(BASE / 'artists.html').write_text(html_page(
    "Gothic Country Artists — Key Artists in the Genre | GothicCountryMusic.com",
    "The essential gothic country artists — Dark Country Boy, Johnny Cash, Nick Cave, Sixteen Horsepower, and more. Discover the musicians who define the gothic country sound.",
    artists_schema, artists_body, "/artists.html"
), encoding='utf-8')
print("✓ artists.html")

# ── SONGS.HTML ─────────────────────────────────────────────────────────────────
songs_schema = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "Essential Gothic Country Songs",
    "description": "The essential gothic country songs — featuring the complete Dark Country Boy catalog.",
    "url": "https://gothiccountrymusic.com/songs.html",
    "numberOfItems": len(tracks),
    "itemListElement": [
        {"@type": "ListItem", "position": i+1, "name": t['trackName'],
         "url": f"https://gothiccountrymusic.com/songs/{t['trackSlug']}.html"}
        for i, t in enumerate(tracks[:50])
    ]
}

song_items = ""
for t in tracks:
    song_items += f'<div class="card"><h3><a href="/songs/{t["trackSlug"]}.html">{t["trackName"]}</a></h3><p style="color:#999;font-size:.85em">{t["albumName"]} · {t["releaseDate"][:4]}</p>{streaming_buttons(t)}</div>\n'

songs_body = f"""<div class="hero">
<h1>Essential Gothic Country Songs</h1>
<p>The dark country canon — all {len(tracks)} songs from Dark Country Boy's gothic country catalog, plus the essential gothic country classics.</p>
</div>
<div class="container">
<p>Gothic country music's power lies in its songs. Murder ballads, dark love songs, spiritual wrestlings, and tales of outlaws and sinners — these are the tracks that define the genre. Below you'll find the complete Dark Country Boy catalog, {len(tracks)} songs of gothic country in its most prolific modern form.</p>
{song_items}
</div>"""

(BASE / 'songs.html').write_text(html_page(
    f"Essential Gothic Country Songs — {len(tracks)} Tracks | GothicCountryMusic.com",
    f"The essential gothic country songs — all {len(tracks)} Dark Country Boy tracks plus the classics that define the genre. Stream on Spotify, Apple Music, YouTube Music, and Amazon Music.",
    songs_schema, songs_body, "/songs.html"
), encoding='utf-8')
print("✓ songs.html")

# ── SONG PAGES ─────────────────────────────────────────────────────────────────
print(f"Generating {len(tracks)} song pages...")

# Build index for related songs (same album or random selection)
album_map = {}
for t in tracks:
    album_map.setdefault(t['albumSlug'], []).append(t)

generated = 0
for i, track in enumerate(tracks):
    # Related songs: prefer same album, fill with random
    same_album = [t for t in album_map[track['albumSlug']] if t['trackSlug'] != track['trackSlug']]
    related = same_album[:4]
    if len(related) < 4:
        others = [t for t in tracks if t['trackSlug'] != track['trackSlug'] and t not in related]
        related += random.sample(others, min(4 - len(related), len(others)))

    related_html = ""
    for r in related[:4]:
        related_html += f'<a href="/songs/{r["trackSlug"]}.html" class="card" style="display:block">{r["trackName"]}<br><small style="color:#999">{r["albumName"]}</small></a>'

    desc = song_description(track['trackName'], track['albumName'])
    
    song_schema = {
        "@context": "https://schema.org",
        "@type": "MusicRecording",
        "name": track['trackName'],
        "byArtist": {
            "@type": "MusicGroup",
            "name": "Dark Country Boy",
            "sameAs": "https://open.spotify.com/artist/4TQMuCjeTbhqvPinWKqRAv"
        },
        "inAlbum": {
            "@type": "MusicAlbum",
            "name": track['albumName']
        },
        "genre": "Gothic Country",
        "datePublished": track['releaseDate'],
        "url": f"https://gothiccountrymusic.com/songs/{track['trackSlug']}.html",
        "image": track['artworkUrl']
    }

    song_body = f"""<div class="hero" style="padding:40px 20px">
<h1>{track['trackName']}</h1>
<p style="color:#999">Dark Country Boy · {track['albumName']} · {track['releaseDate'][:4]}</p>
<img src="{track['artworkUrl']}" alt="{track['albumName']} album art" style="width:200px;height:200px;object-fit:cover;border:2px solid #b8956a;margin:16px auto;display:block">
<div style="margin-top:16px">
{streaming_buttons(track)}
</div>
</div>
<div class="container">
<div class="card">
<h2>About This Song</h2>
<p>{desc}</p>
<p>Released: {track['releaseDate']} · Album: <em>{track['albumName']}</em></p>
</div>

<div class="card">
<h2>Stream "{track['trackName']}"</h2>
<p>Available on all major streaming platforms:</p>
{streaming_buttons(track)}
</div>

<div class="card">
<h2>Related Gothic Country Songs</h2>
<div class="related">
{related_html}
</div>
</div>

<p style="margin-top:20px"><a href="/songs.html">← Browse all gothic country songs</a></p>
</div>"""

    page = html_page(
        f"{track['trackName']} — Dark Country Boy | GothicCountryMusic.com",
        f"Stream {track['trackName']} by Dark Country Boy on Spotify, Apple Music, YouTube Music, and Amazon Music. Gothic country music at its finest.",
        song_schema, song_body,
        f"/songs/{track['trackSlug']}.html"
    )
    (SONGS_DIR / f"{track['trackSlug']}.html").write_text(page, encoding='utf-8')
    generated += 1
    if generated % 200 == 0:
        print(f"  ... {generated}/{len(tracks)} song pages")

print(f"✓ {generated} song pages")

# ── SITEMAP ────────────────────────────────────────────────────────────────────
urls = [
    ("https://gothiccountrymusic.com/", "1.0", "weekly"),
    ("https://gothiccountrymusic.com/what-is-gothic-country.html", "0.9", "monthly"),
    ("https://gothiccountrymusic.com/history.html", "0.9", "monthly"),
    ("https://gothiccountrymusic.com/artists.html", "0.9", "monthly"),
    ("https://gothiccountrymusic.com/songs.html", "0.8", "weekly"),
]
for t in tracks:
    urls.append((f"https://gothiccountrymusic.com/songs/{t['trackSlug']}.html", "0.6", "monthly"))

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url, pri, freq in urls:
    sitemap += f"<url><loc>{url}</loc><priority>{pri}</priority><changefreq>{freq}</changefreq></url>\n"
sitemap += "</urlset>"
(BASE / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
print("✓ sitemap.xml")

# ── ROBOTS.TXT ─────────────────────────────────────────────────────────────────
robots = """User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

Sitemap: https://gothiccountrymusic.com/sitemap.xml
"""
(BASE / 'robots.txt').write_text(robots, encoding='utf-8')
print("✓ robots.txt")

# ── CNAME ──────────────────────────────────────────────────────────────────────
(BASE / 'CNAME').write_text("gothiccountrymusic.com\n", encoding='utf-8')
print("✓ CNAME")

total = len(list(BASE.rglob('*.html')))
print(f"\n✅ Build complete: {total} HTML pages + sitemap + robots + CNAME")
