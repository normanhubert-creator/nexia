# NEXIA — site vitrine

Première version du site vitrine de NEXIA, conçu comme une landing page éditoriale et immersive. Le site présente les quatre formats NEXIA, l’immersion de deux jours, l’expérience scénique Norman + Patrick et un formulaire de prise de contact.

## Stack

- React 18
- Vite
- CSS natif
- Netlify Forms
- Déploiement continu Netlify depuis la branche `main`

Le projet évite volontairement les dépendances d’interface superflues.

- Site public : https://nexia-experience.netlify.app
- Dépôt GitHub : https://github.com/normanhubert-creator/nexia

## Lancer le site

```bash
npm install
npm run dev
```

Le serveur local indique l’adresse à ouvrir, généralement `http://localhost:5173`.

## Build de production

```bash
npm run build
npm run preview
```

Le build est généré dans `dist/`.

## Modifier le site

- Contenu et structure : `src/App.jsx`
- Identité visuelle et responsive : `src/styles.css`
- Métadonnées SEO et détection Netlify Forms : `index.html`
- Photographies : `public/images/`
- Configuration Netlify : `netlify.toml`

Les sources des photographies utilisées sont documentées dans `public/images/PHOTO-SOURCES.md`.

## Déploiement

Netlify exécute automatiquement `npm run build` et publie `dist/` à chaque push sur la branche `main` du dépôt GitHub `normanhubert-creator/nexia`.

Le formulaire `contact` est détecté au moment du build par Netlify. Les soumissions sont visibles dans l’espace Netlify du site.

### Récupérer les messages

Les demandes sont enregistrées dans le tableau de bord Netlify :

`https://app.netlify.com/projects/nexia-experience/forms`

Ouvrir le formulaire `contact` pour consulter et exporter les soumissions. Aucune notification par email n’est encore configurée : l’adresse destinataire doit être choisie avant de l’activer dans **Project configuration → Notifications → Form submission notifications**.

## TODO avant ouverture officielle

- compléter les mentions légales et les informations de l’éditeur ;
- confirmer l’adresse ou la zone géographique à afficher, si souhaité ;
- remplacer ou compléter les projections visuelles par les photographies d’un prochain shooting, si souhaité ;
- configurer les notifications de formulaire vers l’adresse choisie ;
- produire une image Open Graph dédiée si une carte de partage sur mesure est souhaitée.

Ces éléments ne sont pas inventés dans la V1 : ils restent explicitement identifiés comme `TODO`.
