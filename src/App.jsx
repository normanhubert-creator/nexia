import { useEffect, useState } from "react";

const FORMATS = [
  { number: "01", duration: "Une demi-journée", title: "NEXIA Expérience", text: "Un format court et ciblé pour ouvrir le sujet, expérimenter sur quelques cas réels et mettre une équipe en mouvement.", note: "Dirigeants · CODIR · Équipes · Entrepreneurs" },
  { number: "02", duration: "Une journée", title: "NEXIA Expérience", text: "Une respiration complète, entre prise de recul, démonstrations, ateliers et construction de cas d’usage propres à votre activité.", note: "Dans votre entreprise, chez NEXIA ou dans un lieu choisi" },
  { number: "03", duration: "Deux jours", title: "NEXIA Immersion", text: "L’expérience emblématique : un petit groupe, un lieu à part et le temps nécessaire pour comprendre, créer et repartir avec du concret.", note: "Format intensif · Hébergement possible", featured: true },
  { number: "04", duration: "Sur scène", title: "NEXIA Live", text: "Une conférence-expérience à deux voix où expertise, humour et mise en situation se répondent pour parler autrement de l’IA.", note: "Conférences · Événements · Lieux remarquables" },
];

const METHOD = [
  ["Comprendre", "Prendre de la hauteur sans perdre le lien avec votre réalité."],
  ["Expérimenter", "Manipuler, tester et confronter les possibilités aux usages."],
  ["Construire", "Créer des cas, outils ou méthodes directement utiles."],
  ["Passer à l’action", "Choisir les prochains pas et les inscrire dans le temps."],
];

function Mark() {
  return <span className="mark" aria-label="NEXIA">NE<span>X</span>IA</span>;
}

function Arrow() {
  return <span aria-hidden="true">↘</span>;
}

function ContactForm() {
  const [state, setState] = useState("idle");

  const submit = async (event) => {
    event.preventDefault();
    setState("sending");
    const form = event.currentTarget;
    try {
      await fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(new FormData(form)).toString(),
      });
      form.reset();
      setState("sent");
    } catch {
      setState("error");
    }
  };

  if (state === "sent") {
    return (
      <div className="form-success" role="status">
        <p className="eyebrow">Message transmis</p>
        <h3>Merci. La conversation peut commencer.</h3>
        <p>Votre demande a bien été enregistrée. Norman et Patrick reviendront vers vous.</p>
        <button className="text-link" type="button" onClick={() => setState("idle")}>Envoyer une autre demande</button>
      </div>
    );
  }

  return (
    <form className="contact-form" name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" onSubmit={submit}>
      <input type="hidden" name="form-name" value="contact" />
      <p className="hidden-field"><label>Ne pas remplir : <input name="bot-field" /></label></p>
      <div className="field-grid">
        <label>Prénom / nom<input name="name" type="text" autoComplete="name" required /></label>
        <label>Entreprise<input name="company" type="text" autoComplete="organization" required /></label>
        <label>Email<input name="email" type="email" autoComplete="email" required /></label>
        <label>Téléphone <span>(facultatif)</span><input name="phone" type="tel" autoComplete="tel" /></label>
        <label>Format envisagé<select name="format" defaultValue="" required><option value="" disabled>Choisir un format</option><option>Demi-journée</option><option>Journée</option><option>Immersion deux jours</option><option>Conférence / événement</option><option>À construire ensemble</option></select></label>
        <label>Nombre de personnes<input name="people" type="number" min="1" inputMode="numeric" required /></label>
      </div>
      <label>Parlez-nous de votre besoin<textarea name="message" rows="5" required /></label>
      <div className="form-bottom">
        <p>Les informations transmises servent uniquement à répondre à votre demande.</p>
        <button className="button button--cream" type="submit" disabled={state === "sending"}>{state === "sending" ? "Envoi…" : "Parler de votre projet"}<Arrow /></button>
      </div>
      {state === "error" && <p className="form-error" role="alert">L’envoi n’a pas abouti. Merci de réessayer dans quelques instants.</p>}
    </form>
  );
}

export default function App() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    const elements = document.querySelectorAll("[data-reveal]");
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => entry.isIntersecting && entry.target.classList.add("is-visible"));
    }, { threshold: 0.14 });
    elements.forEach((element) => observer.observe(element));
    return () => observer.disconnect();
  }, []);

  const closeMenu = () => setMenuOpen(false);

  return (
    <main>
      <header className={`${scrolled ? "nav nav--solid" : "nav"} ${menuOpen ? "nav--open" : ""}`}>
        <a className="logo" href="#accueil" onClick={closeMenu}><Mark /></a>
        <button className="menu-toggle" type="button" aria-expanded={menuOpen} aria-controls="main-navigation" onClick={() => setMenuOpen((open) => !open)}>
          <span>{menuOpen ? "Fermer" : "Menu"}</span><i aria-hidden="true" />
        </button>
        <nav id="main-navigation" aria-label="Navigation principale">
          <a href="#experiences" onClick={closeMenu}>Expériences</a><a href="#immersion" onClick={closeMenu}>Immersion</a><a href="#live" onClick={closeMenu}>Live</a><a href="#apropos" onClick={closeMenu}>À propos</a><a href="#contact" onClick={closeMenu}>Nous contacter</a>
        </nav>
      </header>

      <section className="hero" id="accueil">
        <img src="/images/hero-stone-courtyard.jpg" alt="Cour intérieure en pierre, cadre d’une expérience NEXIA" />
        <div className="hero__veil" />
        <div className="hero__content">
          <p className="eyebrow">Expériences d’intelligence artificielle</p>
          <h1>Faire vivre l’IA.<br /><em>Vraiment.</em></h1>
          <div className="hero__footer">
            <p>Quelques heures, une journée ou deux jours hors du quotidien pour comprendre, expérimenter et construire votre propre manière de travailler avec l’intelligence artificielle.</p>
            <a className="button button--light" href="#experiences">Découvrir les expériences <Arrow /></a>
          </div>
        </div>
        <p className="hero__note">NEXT + IA</p>
      </section>

      <section className="intro section-pad" id="experiences">
        <p className="eyebrow eyebrow--dark" data-reveal>Une autre manière d’entrer dans le sujet</p>
        <p className="intro__lead" data-reveal>Ce n’est pas une conférence de plus.<br />Ce n’est pas une formation comme les autres.</p>
        <div className="intro__aside" data-reveal>
          <span>01 — La promesse</span>
          <p>NEXIA crée un temps privilégié pour comprendre ce qui change, éprouver les outils sur le terrain et fabriquer une réponse qui vous appartient. L’IA y devient une expérience professionnelle et humaine — jamais un catalogue de recettes.</p>
          <a className="text-link" href="#contact">Imaginer mon format <Arrow /></a>
        </div>
      </section>

      <section className="formats section-pad">
        <div className="section-heading" data-reveal><p className="eyebrow">Quatre manières de vivre NEXIA</p><h2>Le bon format est celui qui vous fait avancer.</h2></div>
        <div className="format-list">
          {FORMATS.map((format) => (
            <article className={`format-card ${format.featured ? "format-card--featured" : ""}`} key={format.number} data-reveal>
              <span className="format-card__number">{format.number}</span>
              <div><p className="format-card__duration">{format.duration}</p><h3>{format.title}</h3></div>
              <p className="format-card__text">{format.text}</p><p className="format-card__note">{format.note}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="personalization">
        <div className="personalization__copy section-pad" data-reveal>
          <p className="eyebrow">Sur mesure, dès le départ</p><h2>Votre expérience commence avant notre rencontre.</h2>
          <p>Votre métier, votre niveau, vos outils, vos questions et vos irritants dessinent le contenu. Un questionnaire, un échange préparatoire et l’identification de cas réels nous permettent d’arriver avec un temps qui vous ressemble — exigeant sur le fond, immédiatement mobilisable dans la pratique.</p>
          <ul><li>Vos situations, pas des cas génériques</li><li>Un rythme ajusté au groupe</li><li>Des réalisations utiles après la rencontre</li></ul>
        </div>
        <figure className="personalization__image"><img src="/images/workshop-room-premium.jpg" alt="Salle de travail NEXIA préparée avec tables en bois, carnets et assises chaleureuses" loading="lazy" /><figcaption>Un cadre préparé pour votre réalité.</figcaption></figure>
      </section>

      <section className="method section-pad">
        <div className="section-heading section-heading--split" data-reveal><p className="eyebrow eyebrow--dark">Le mouvement NEXIA</p><h2>De la curiosité<br />à quelque chose de concret.</h2></div>
        <ol className="method-grid">{METHOD.map(([title, text], index) => <li key={title} data-reveal><span>{String(index + 1).padStart(2, "0")}</span><h3>{title}</h3><p>{text}</p></li>)}</ol>
      </section>

      <section className="immersion" id="immersion">
        <div className="immersion__visual"><img src="/images/immersion-pond-premium.jpg" alt="Table en bois préparée au bord de l’eau dans le lieu d’immersion NEXIA" loading="lazy" /><p>Deux jours<br />hors du quotidien</p></div>
        <div className="immersion__copy section-pad" data-reveal>
          <p className="eyebrow">NEXIA Immersion</p><h2>Changer de cadre pour changer de perspective.</h2>
          <p className="large-copy">Un petit groupe, un lieu à part, des temps de travail et des respirations. L’immersion donne de la place aux questions qui comptent et aux échanges que l’agenda ordinaire empêche.</p>
          <div className="immersion__details"><p><strong>Avant</strong><span>Questionnaire, entretien et préparation de cas adaptés.</span></p><p><strong>Pendant</strong><span>Compréhension, expérimentation, construction, repas et échanges informels.</span></p><p><strong>Après</strong><span>Des éléments personnalisés et une projection à 30 / 60 / 90 jours.</span></p></div>
          <a className="button button--outline" href="#contact">Organiser une immersion <Arrow /></a>
        </div>
      </section>

      <section className="place section-pad">
        <div className="place__intro" data-reveal><p className="eyebrow eyebrow--dark">Le lieu fait partie de l’expérience</p><h2>Du calme. De la lumière.<br />Et du temps pour penser.</h2></div>
        <div className="place__gallery"><figure className="place__large"><img src="/images/place-house-pool.jpg" alt="Maison en pierre et espace extérieur du lieu NEXIA" loading="lazy" /></figure><figure className="place__small"><img src="/images/grounds-pond.jpg" alt="Étang et nature autour du lieu d’immersion" loading="lazy" /></figure><p data-reveal>Intérieurs accueillants, table partagée, espaces extérieurs et hébergement possible : le décor ne se contente pas d’accueillir l’expérience, il lui donne son rythme.</p></div>
      </section>

      <section className="live" id="live">
        <div className="live__copy section-pad" data-reveal>
          <p className="eyebrow">NEXIA Live</p><h2>L’IA entre<br /><em>en scène.</em></h2>
          <p>Une conférence à deux voix où expertise, humour et mise en situation se répondent pour parler autrement de l’intelligence artificielle.</p>
          <p>Norman apporte les repères de la recherche et des systèmes humain‑IA. Patrick mobilise son expérience pédagogique, entrepreneuriale et son art du décalage. Leur dialogue rend les idées plus claires, plus mémorables et plus faciles à mettre en mouvement — sans transformer le propos en spectacle de stand-up.</p>
          <a className="button button--light" href="#contact">Imaginer votre événement <Arrow /></a>
        </div>
        <figure className="live__visual"><img src="/images/live-norman-patrick.jpg" alt="Norman Hubert et Patrick Martinez lors d’une conférence NEXIA à deux voix" loading="lazy" /><figcaption>Projection visuelle de l’expérience NEXIA Live</figcaption></figure>
      </section>

      <section className="hosts section-pad" id="apropos">
        <div className="section-heading section-heading--split" data-reveal><p className="eyebrow eyebrow--dark">Vos hôtes</p><h2>Deux regards.<br />Une expérience à construire.</h2></div>
        <div className="hosts__grid">
          <article className="host-card" data-reveal><div className="host-card__portrait host-card__portrait--norman"><img src="/images/live-norman-patrick.jpg" alt="Norman Hubert" loading="lazy" /></div><div><p className="host-card__role">Co-fondateur · Recherche & usages</p><h3>Norman Hubert</h3><p className="host-card__bio">Doctorant en sciences de gestion et du management et enseignant à l’Université Paris‑Panthéon‑Assas, Norman étudie les transformations du travail liées à l’IA générative et les nouvelles collaborations humain‑IA. Chez NEXIA, il apporte les repères, la méthode et l’exigence de vérification.</p><a className="text-link" href="https://www.linkedin.com/in/norman-hubert/" target="_blank" rel="noreferrer">Profil LinkedIn <span aria-hidden="true">↗</span></a></div></article>
          <article className="host-card" data-reveal><div className="host-card__portrait host-card__portrait--patrick"><img src="/images/live-norman-patrick.jpg" alt="Patrick Martinez" loading="lazy" /></div><div><p className="host-card__role">Co-fondateur · Pédagogie & expérience</p><h3>Patrick Martinez</h3><p className="host-card__bio">Formateur indépendant depuis plus de dix ans, Patrick intervient en création et gestion d’entreprise, stratégie financière, négociation et entrepreneuriat. Certifié Coach Manager, il apporte à NEXIA l’écoute, la mise en mouvement et une expérience pédagogique profondément ancrée dans le terrain.</p><a className="text-link" href="https://www.linkedin.com/in/patrick-martinez-121a1291/" target="_blank" rel="noreferrer">Profil LinkedIn <span aria-hidden="true">↗</span></a></div></article>
        </div>
      </section>

      <section className="horizon section-pad">
        <p className="eyebrow">NEXIA, aujourd’hui et demain</p>
        <div className="horizon__grid"><p><strong>Immersion</strong><span>Les expériences intensives et résidentielles.</span></p><p><strong>Academy</strong><span>Les programmes pédagogiques premium.</span></p><p><strong>Business</strong><span>L’expérience NEXIA au sein de votre organisation.</span></p><p className="horizon__future"><strong>Campus</strong><span>Une ambition à plus long terme pour un lieu permanent consacré à l’IA.</span></p></div>
      </section>

      <section className="contact section-pad" id="contact">
        <div className="contact__heading" data-reveal><p className="eyebrow">La prochaine étape</p><h2>Et si votre prochaine étape commençait ici ?</h2><p>Parlez-nous de votre contexte. Nous imaginerons ensemble le format, le lieu et le rythme les plus justes.</p></div>
        <ContactForm />
      </section>

      <footer className="footer"><a href="#accueil" className="footer__logo"><Mark /></a><p>L’intelligence artificielle pour passer à l’étape suivante.</p><div><a href="#experiences">Expériences</a><a href="#immersion">Immersion</a><a href="#live">Live</a><a href="#contact">Contact</a></div><p className="footer__legal">© {new Date().getFullYear()} NEXIA · <strong>TODO</strong> — Mentions légales à compléter avant ouverture officielle.</p></footer>
    </main>
  );
}
