---
description: "Création de la page de profil utilisateur avec mise à jour des informations et upload d'avatar sécurisé."
icon: lucide/book-open-check
tags: ["LARAVEL", "BREEZE", "PROJET GUIDÉ"]
---

# Phase 4 — Profil Utilisateur & Upload

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Laravel 11"
  data-time="~1 heure">
</div>

## Objectifs de la Phase 4

!!! info "Ce que vous allez faire"
    - Étendre la page Profil générée par Breeze
    - Ajouter un champ `bio` éditable
    - Implémenter l'upload d'avatar sécurisé
    - Valider les fichiers côté serveur (type MIME, taille max)

## Mise à Jour du ProfileController

```php title="app/Http/Controllers/ProfileController.php (méthode update)"
public function update(ProfileUpdateRequest $request): RedirectResponse
{
    $validated = $request->validated();

    // Upload de l'avatar si fourni
    if ($request->hasFile('avatar')) {
        // Supprimer l'ancien avatar
        if ($request->user()->avatar) {
            Storage::disk('public')->delete($request->user()->avatar);
        }

        $path = $request->file('avatar')->store('avatars', 'public');
        $validated['avatar'] = $path;
    }

    $request->user()->fill($validated)->save();

    return Redirect::route('profile.edit')->with('status', 'profile-updated');
}
```

## Validation — ProfileUpdateRequest

```php title="app/Http/Requests/ProfileUpdateRequest.php"
public function rules(): array
{
    return [
        'name'   => ['required', 'string', 'max:255'],
        'email'  => ['required', 'email', 'max:255', Rule::unique(User::class)->ignore($this->user()->id)],
        'bio'    => ['nullable', 'string', 'max:500'],
        'avatar' => ['nullable', 'image', 'mimes:jpg,jpeg,png,webp', 'max:2048'], // 2 Mo max
    ];
}
```

## Vue Profil — Champ Avatar

```html title="resources/views/profile/partials/update-profile-information-form.blade.php (extrait)"
<form method="post" action="{{ route('profile.update') }}" enctype="multipart/form-data">
    @csrf
    @method('patch')

    <!-- Avatar actuel -->
    @if (Auth::user()->avatar)
        <img src="{{ Storage::url(Auth::user()->avatar) }}" class="w-20 h-20 rounded-full" alt="Avatar">
    @endif

    <!-- Upload nouvel avatar -->
    <x-input-label for="avatar" value="Avatar (JPG, PNG, WebP - 2 Mo max)" />
    <input type="file" name="avatar" id="avatar" accept="image/*" class="mt-1">
    <x-input-error :messages="$errors->get('avatar')" />
</form>
```


<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    L'upload de fichiers est un vecteur d'attaque classique. La validation `mimes:jpg,jpeg,png,webp` ne vérifie pas seulement l'extension — elle lit les octets du fichier (magic bytes). La limite de taille (`max:2048`) protège contre les attaques de déni de service par fichiers volumineux. Ces deux règles sont non négociables sur toute implémentation d'upload en production.

> [Phase 5 — Autorisation et protection des routes →](./phase5.md)
