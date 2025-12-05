# Plan d'Automatisation des Emails - Subly

**Date de création :** 5 décembre 2025
**Objectif :** Automatiser l'envoi d'emails aux utilisateurs pour proposer des appels de feedback et mieux comprendre les besoins de la cible

---

## 🎯 Contexte

Actuellement, les emails sont envoyés **manuellement** à chaque nouvel utilisateur. Avec l'augmentation du nombre d'inscriptions, ce processus devient trop chronophage et nécessite une automatisation.

**Objectif des emails :** Proposer aux utilisateurs un appel de 30 minutes pour :
- Comprendre leur parcours d'apprentissage des langues
- Recueillir des feedbacks sur l'extension Subly
- Offrir de la valeur en échange (accès à vie, cours de français, etc.)

---

## 📧 Les 3 Scénarios d'Emails

### Scénario 1 : Inscription sans carte bancaire (après 2h)
**Timing :** 2 heures après l'inscription
**Condition :** L'utilisateur s'est inscrit avec Google OAuth MAIS n'a pas entré sa carte bancaire
**Email :** Offre d'accès à vie gratuit en échange de 30 minutes d'appel

### Scénario 2 : Annulation pendant l'essai gratuit (immédiat)
**Timing :** Immédiatement après l'annulation
**Condition :** L'utilisateur a mis sa carte, commencé l'essai gratuit (3 jours), puis annulé AVANT la première facturation
**Email :** Demande de feedback pour comprendre pourquoi l'extension ne convenait pas

### Scénario 3 : Première facturation (immédiat)
**Timing :** Immédiatement après la première facturation (jour 3 après début trial)
**Condition :** L'utilisateur a mis sa carte et a été facturé $9 (n'a pas annulé pendant le trial)
**Email :** Remerciement + offre de cours de français en échange de 30 minutes d'appel

---

## 🏗️ Architecture Technique

### Scénario 1 : Vercel Cron Job
- **Fréquence :** Toutes les heures
- **Vérification :** Utilisateurs inscrits il y a 2-3h sans `stripe_customer_id` et sans `trial_reminder_sent_at` et sans `had_subscription`
- **Action :** Envoi email + marquage `trial_reminder_sent_at = NOW()`

### Scénarios 2 & 3 : Webhooks Stripe
- **Webhook existant :** `/api/stripe/webhook/route.ts`
- **Événements à ajouter :**
  - `customer.subscription.deleted` (scénario 2 - annulation pendant trial uniquement)
  - `invoice.paid` (scénario 3 - première facturation uniquement)

### Service d'envoi : Resend
- **Configuration :**
  - `from: 'Ulysse from Subly <ulysse@sublyy.com>'`
  - `replyTo: 'unducamp.pro@gmail.com'`
- **Avantage :** Les utilisateurs peuvent cliquer "Reply" et leur email sera automatiquement dirigé vers `unducamp.pro@gmail.com`
- **Tracking :** Activé (inclus gratuitement dans Resend - ouvertures et clics)

---

## 🗄️ Modifications Base de Données (Supabase)

### Table `users`
Ajouter 2 nouvelles colonnes :

```sql
ALTER TABLE users
ADD COLUMN trial_reminder_sent_at TIMESTAMPTZ,
ADD COLUMN had_subscription BOOLEAN DEFAULT FALSE;
```

**Explications :**
- `trial_reminder_sent_at` : Timestamp d'envoi de l'email scénario 1 (évite les doublons)
- `had_subscription` : Flag pour éviter d'envoyer l'email scénario 1 aux utilisateurs qui ont déjà eu une subscription puis annulé rapidement

---

## 📝 Templates d'Emails

### Email 1 : Inscription sans carte (après 2h)

**Objet :**
```
You're officially the 49th person who signed up for Subly
```

**Corps :**
```
Hello, It's Ulysse, the developer behind the Subly Netflix extension

I saw you registered for Subly, thanks a lot for your interest in our tool! It's the very beginning of our extension and you are officially the 49th person who signed up.

I noticed that you didn't start the free trial, I totally understand you, since you have to enter your credit card to start it.

Even though you didn't start the free trial, I would really like to hear your thoughts about the extension. Things like what motivated you to download it and register, what were your expectations from it, things like that. I would also like to learn about your language learning journey to understand better who can be interested by Subly and what pain points we could solve.

I believe that a call is worth a thousand emails, I'd like to propose you something:

→ I offer you a totally free subscription, lifetime, for Subly and in exchange you give 30mn of your time to talk through a video call about your language learning journey and your thoughts about the extension.

I've already had 8 calls like that and the conversations are always very interesting, it's such a pleasure to exchange with other language learners and getting feedback about Subly is extremely valuable for us. Having calls with potential users like you is very important at this stage because it allows us to really understand your needs and how we can address them.

I believe that a free lifetime subscription to Subly is a very good gift since we plan to add a lot of features to Subly to turn it into a very complete language learning solution. We really want to make language learning easier and smoother.

During our call, I'll also do my best to help you as much as I can in your learning process by giving you tips and tools to try, depending on your constraints and goals (I know a lot about language learning tools, that's why we decided to create our own)

I know from experience that just one tip can often change a whole language learning trajectory and make the difference between a habit that you give up early and one that you maintain over the long-term. Language learning shouldn't be hard.

It's only because it's the very beginning of Subly that I am offering this kind of deal, I don't know for how long I'll propose calls like that.

If you're ok to give 30mn of your time to help us and play a role in the development of Subly, you can book a call with me directly through this link at the most convenient moment for you: https://calendly.com/ulysse-i/30min (It will automatically create a google meet link for us to have the call at the time you picked)

Thanks a lot for your time,

Ulysse Ducamp
```

---

### Email 2 : Annulation pendant trial

**Objet :**
```
You canceled your subscription and that's ok
```

**Corps :**
```
Hello, it's Ulysse, the developer behind Subly!

I saw that you tested Subly and canceled your subscription (which is totally ok). I am very sorry that Subly didn't match your expectations. I just launched this extension (you are actually the 9th person who entered their credit card) and I'd love to hear your feedback about Subly to know what I should improve/add/correct first.

I'd be extremely grateful if you could answer to this email with a quick feedback 🙏

Thanks a lot for your precious time,

Ulysse Ducamp
```

---

### Email 3 : Première facturation

**Objet :**
```
You're officially Subly's 8th customer!
```

**Corps :**
```
Hello, it's Ulysse, the developer behind Subly.

Thank you so much for your interest in our extension. It's far from being perfect but it's a beginning and you are officially our 8th customer which is very important to us.

I would really like to hear your thoughts about the extension. Things like what motivated you to register, what were your expectations from it, things like that. I would also like to learn about your language learning journey to understand better who can be interested by Subly and what pain points we could solve.

I believe that a call is worth a thousand emails, I'd like to propose you something, as a french native (born and raised in Paris), I offer you a free 30mn French tutoring call and in exchange you give 30mn of your time to talk about your language learning journey and your thoughts about the extension through a video call.

I've already had 4 calls like that and the conversations are always very interesting, it's such a pleasure to exchange with other language learners and getting feedback about Subly is extremely valuable for us. Having calls with users like you is very important at this stage because it allows us to really understand your needs.

This call will have a real impact on how Subly is shaped, you'll be able to propose ideas that we will really listen to. We plan to add a lot of innovative features to Subly. We really want to make language learning easier and smoother and we need your help (30mn of your time) for that.

During our call, I'll also do my best to help you as much as I can in your learning process by giving you tips and tools to try, depending on your constraints and goals (I know a lot about language learning tools, that's why we decided to create our own).

I know from experience that just one tip can often change a whole language learning trajectory and make the difference between a habit that you give up early and one that you maintain over the long-term. Language learning shouldn't be hard.

It's only because it's the very beginning of Subly that I am offering this kind of "deal", I don't know for how long I'll propose calls like that.

If you're ok to give 30mn of your time to help us, you can book a call with me directly through this link at the most convenient moment for you: https://calendly.com/ulysse-i/30min

(After the call, you'll be able to book another call for our 30min French tutoring call as promised)

Thanks a lot for your time,

Ulysse Ducamp
```

---

## 🔑 Décisions Clés

### Email Configuration
- ✅ **From :** `Ulysse from Subly <ulysse@sublyy.com>`
- ✅ **Reply-To :** `unducamp.pro@gmail.com`
- ✅ **Tracking :** Activé (gratuit dans Resend)
- ✅ **Liens :** Texte brut (pas de boutons HTML)

### Numéros dans les emails
- ✅ **Statiques** : "49th person", "9th person", "8th customer" restent hardcodés
- ✅ **Pas de calcul dynamique** pour éviter la complexité
- ✅ L'objectif est de montrer qu'on est au début, le chiffre exact n'est pas critique

### Gestion des erreurs
- ✅ **Silent fail** : Si Resend échoue, on log l'erreur mais on marque quand même `trial_reminder_sent_at`
- ✅ Pas de retry logic pour l'instant (KISS principe)
- ✅ On pourra améliorer plus tard si nécessaire

### Edge Cases
- ✅ **Utilisateur met sa carte puis annule dans les 2h** : Reçoit Email 2 uniquement (pas Email 1) grâce au flag `had_subscription`
- ✅ **Utilisateur met sa carte après avoir reçu Email 1** : Ne reçoit plus Email 1 aux prochaines exécutions du Cron (condition `stripe_customer_id` non remplie)

### Ce qu'on NE fait PAS (YAGNI)
- ❌ Pas de timezone logic (on envoie 2h après quoi qu'il arrive)
- ❌ Pas de table `email_logs` (Resend Dashboard suffit)
- ❌ Pas de retry logic complexe
- ❌ Pas de feature flag pour désactiver les emails
- ❌ Pas de différenciation entre annulation trial vs annulation post-facturation (pour l'instant, Email 2 = uniquement trial)

---

## ✅ Checklist d'Implémentation

### Phase 1 : Modifications Base de Données
- [ ] Créer une migration Supabase pour ajouter les colonnes `trial_reminder_sent_at` et `had_subscription` à la table `users`
- [ ] Appliquer la migration en staging
- [ ] Vérifier que les colonnes existent dans Supabase Dashboard
- [ ] Appliquer la migration en production

### Phase 2 : Templates d'Emails
- [ ] Créer `webapp-next/src/lib/emails/templates.ts` avec les 3 templates HTML
- [ ] Créer `webapp-next/src/lib/emails/sendEmail.ts` avec helper centralisé Resend
- [ ] Tester l'import des templates dans une route test

### Phase 3 : Vercel Cron (Scénario 1)
- [ ] Créer `webapp-next/src/app/api/cron/trial-reminder/route.ts`
- [ ] Implémenter la logique :
  - [ ] Query Supabase : users créés il y a 2-3h, sans `stripe_customer_id`, sans `trial_reminder_sent_at`, sans `had_subscription`
  - [ ] Boucle sur les utilisateurs trouvés
  - [ ] Envoyer email via Resend (template 1)
  - [ ] Mettre à jour `trial_reminder_sent_at = NOW()`
  - [ ] Logger succès/erreurs
- [ ] Configurer `vercel.json` avec le cron schedule (toutes les heures)
- [ ] Tester localement avec des données de test
- [ ] Déployer en staging
- [ ] Vérifier les logs Vercel après 1h d'exécution

### Phase 4 : Webhooks Stripe (Scénarios 2 & 3)
- [ ] Modifier `webapp-next/src/app/api/stripe/webhook/route.ts`
- [ ] Ajouter case `customer.subscription.deleted` :
  - [ ] Vérifier que le statut de la subscription était `trialing` (pas `active`)
  - [ ] Envoyer email via Resend (template 2)
  - [ ] Mettre à jour `had_subscription = TRUE` pour l'utilisateur
  - [ ] Logger l'envoi
- [ ] Ajouter case `invoice.paid` :
  - [ ] Vérifier que c'est la première facturation (pas un renouvellement)
  - [ ] Envoyer email via Resend (template 3)
  - [ ] Logger l'envoi
- [ ] Tester en local avec Stripe CLI webhook forwarding
- [ ] Vérifier les logs Stripe webhook en staging
- [ ] Déployer en production

### Phase 5 : Configuration Resend
- [ ] Vérifier que `sublyy.com` est bien vérifié dans Resend Dashboard
- [ ] Activer le tracking (opens + clicks) dans les paramètres Resend
- [ ] Tester l'envoi d'un email depuis `ulysse@sublyy.com` avec `replyTo` vers `unducamp.pro@gmail.com`
- [ ] Vérifier que la réponse arrive bien dans Gmail

### Phase 6 : Tests de Bout en Bout
- [ ] **Test Scénario 1 :**
  - [ ] Créer un user test dans Supabase (sans `stripe_customer_id`)
  - [ ] Modifier `created_at` pour simuler 2h dans le passé
  - [ ] Déclencher le Cron manuellement ou attendre 1h
  - [ ] Vérifier réception email
  - [ ] Vérifier que `trial_reminder_sent_at` est rempli
  - [ ] Re-déclencher le Cron → vérifier qu'aucun doublon n'est envoyé
- [ ] **Test Scénario 2 :**
  - [ ] Créer un user test avec subscription en `trialing`
  - [ ] Utiliser Stripe CLI pour simuler `customer.subscription.deleted`
  - [ ] Vérifier réception email
  - [ ] Vérifier que `had_subscription = TRUE`
- [ ] **Test Scénario 3 :**
  - [ ] Créer un user test avec subscription en `trialing`
  - [ ] Utiliser Stripe CLI pour simuler `invoice.paid` (première facture)
  - [ ] Vérifier réception email
- [ ] **Test Reply-To :**
  - [ ] Recevoir un des emails de test
  - [ ] Cliquer "Reply" dans le client email
  - [ ] Vérifier que le destinataire est `unducamp.pro@gmail.com`
  - [ ] Envoyer la réponse
  - [ ] Vérifier réception dans Gmail

### Phase 7 : Monitoring & Déploiement Production
- [ ] Vérifier les logs Vercel pour le Cron en staging (24h d'observation)
- [ ] Vérifier les logs Stripe webhook en staging (quelques jours d'observation)
- [ ] Merger dans `main` pour déploiement production
- [ ] Configurer les Cron Vercel en production
- [ ] Vérifier les webhooks Stripe production
- [ ] Observer les logs pendant 48h
- [ ] Vérifier dans Resend Dashboard que les emails sont bien envoyés et ouverts

### Phase 8 : Documentation & Cleanup
- [ ] Mettre à jour CLAUDE.md avec la nouvelle fonctionnalité
- [ ] Ajouter des commentaires dans le code pour expliquer la logique
- [ ] Supprimer les logs de debug excessifs si nécessaire
- [ ] Archiver ce document (EMAIL_AUTOMATION_PLAN.md) dans un dossier `docs/`

---

## 📊 Métriques à Surveiller (Resend Dashboard)

- **Taux d'envoi** : Combien d'emails envoyés par jour/semaine
- **Taux d'ouverture** : % d'emails ouverts (objectif : >30%)
- **Taux de clic** : % de clics sur le lien Calendly (objectif : >10%)
- **Taux de bounce** : % d'emails non délivrés (objectif : <2%)
- **Taux de spam** : % d'emails marqués comme spam (objectif : <0.5%)

---

## 🚨 Points d'Attention

### Scénario 2 : Distinction trial vs post-facturation
**Problème :** Le webhook `customer.subscription.deleted` est envoyé pour toutes les annulations (pendant trial ET après facturation).

**Solution actuelle :** On vérifie que le statut de la subscription était `trialing` avant l'annulation.

**Code à implémenter :**
```typescript
// Dans le webhook customer.subscription.deleted
const subscription = event.data.object as Stripe.Subscription

// Ne send email QUE si c'était en trial
if (subscription.status === 'canceled' && previousStatus === 'trialing') {
  // Envoyer Email 2
}
```

**Note :** Stripe n'inclut pas le `previousStatus` dans le webhook. Il faudra donc vérifier dans la table `subscriptions` de Supabase quel était le statut avant l'annulation, ou vérifier si l'utilisateur a déjà été facturé via `invoice.paid`.

### Scénario 3 : Première facturation uniquement
**Problème :** Le webhook `invoice.paid` est envoyé à chaque facturation (première ET renouvellements mensuels/annuels).

**Solution :** Vérifier que c'est la première facture :
- `invoice.billing_reason === 'subscription_cycle'` ET
- C'est la première facture pour cette subscription (vérifier dans Supabase si on a déjà envoyé l'email, ou compter les factures)

**Code à implémenter :**
```typescript
// Dans le webhook invoice.paid
const invoice = event.data.object as Stripe.Invoice

// Ne send email QUE si c'est la première facturation
if (invoice.billing_reason === 'subscription_cycle' && isFirstInvoice) {
  // Envoyer Email 3
}
```

---

## 🔄 Améliorations Futures (Hors Scope)

Ces améliorations pourront être ajoutées plus tard si nécessaire :

- [ ] Retry logic avec backoff exponentiel pour les échecs d'envoi
- [ ] Table `email_logs` pour tracer tous les emails dans Supabase
- [ ] Feature flag pour désactiver temporairement les emails
- [ ] Timezone-aware sending (envoyer pendant les heures ouvrables)
- [ ] A/B testing des templates d'emails
- [ ] Numéros dynamiques ("Xth person") au lieu de statiques
- [ ] Email différent pour annulation post-facturation (vs annulation trial)
- [ ] Webhook Resend pour tracer opens/clicks dans Supabase

---

## 📚 Ressources

- **Resend Docs :** https://resend.com/docs
- **Stripe Webhooks :** https://stripe.com/docs/webhooks
- **Vercel Cron :** https://vercel.com/docs/cron-jobs
- **Supabase Migrations :** https://supabase.com/docs/guides/database/migrations

---

**Document créé le 5 décembre 2025**
**Dernière mise à jour :** 5 décembre 2025
