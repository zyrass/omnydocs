---
description: "Architecture 03 — Patterns pratiques : Repository, Service Layer, Factory, Observer/Event, CQRS et bonnes pratiques de composition."
icon: lucide/book-open-check
tags: ["ARCHITECTURE", "PATTERNS", "REPOSITORY", "SERVICE", "FACTORY", "OBSERVER", "CQRS"]
---

# Module 03 — Patterns Pratiques

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="2024"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Bibliothèque de Recettes"
    Un cuisinier expérimenté ne réinvente pas ses techniques à chaque plat. Il dispose d'un répertoire de techniques éprouvées (la julienne, la brunoise, la réduction) qu'il applique selon la situation. Les **design patterns** sont ces techniques culinaires du code : des solutions éprouvées à des problèmes récurrents. Vous ne les inventez pas — vous les reconnaissez et les appliquez.

<br>

---

## 1. Repository Pattern

```typescript title="TypeScript — Repository Pattern : abstraction de la persistance"
// ─── Interface (Port) ─────────────────────────────────────────────────────────
interface UserRepository {
    findById(id: string):  Promise<User | null>;
    findByEmail(email: string): Promise<User | null>;
    findAll():             Promise<User[]>;
    save(user: User):      Promise<void>;
    delete(id: string):    Promise<void>;
}

// ─── Implémentation SQL (Adapter Prisma) ──────────────────────────────────────
class PrismaUserRepository implements UserRepository {
    constructor(private prisma: PrismaClient) {}

    async findById(id: string) {
        const data = await this.prisma.user.findUnique({ where: { id } });
        return data ? User.reconstitute(data) : null;
    }

    async findByEmail(email: string) {
        const data = await this.prisma.user.findUnique({ where: { email } });
        return data ? User.reconstitute(data) : null;
    }

    async findAll() {
        const rows = await this.prisma.user.findMany();
        return rows.map(User.reconstitute);
    }

    async save(user: User) {
        await this.prisma.user.upsert({
            where:  { id: user.id },
            create: user.toPersistence(),
            update: user.toPersistence(),
        });
    }

    async delete(id: string) {
        await this.prisma.user.delete({ where: { id } });
    }
}

// ─── Implémentation InMemory (pour les tests) ─────────────────────────────────
class InMemoryUserRepository implements UserRepository {
    private store = new Map<string, User>();

    async findById(id: string)        { return this.store.get(id) ?? null; }
    async findByEmail(e: string)      { return [...this.store.values()].find(u => u.email === e) ?? null; }
    async findAll()                   { return [...this.store.values()]; }
    async save(user: User)            { this.store.set(user.id, user); }
    async delete(id: string)          { this.store.delete(id); }
}
```

<br>

---

## 2. Service Layer Pattern

```typescript title="TypeScript — Service Layer : orchestrer la logique métier"
// Le Service Layer orchestre plusieurs repositories et opérations
class UserService {
    constructor(
        private readonly userRepo:  UserRepository,
        private readonly emailSvc:  EmailService,
        private readonly hashSvc:   HashingService,
    ) {}

    async registerUser(input: RegisterInput): Promise<UserDTO> {
        // 1. Vérifier l'unicité de l'email
        const existing = await this.userRepo.findByEmail(input.email);
        if (existing) {
            throw new ConflictError("Cet email est déjà utilisé");
        }

        // 2. Hacher le mot de passe
        const hashedPassword = await this.hashSvc.hash(input.password);

        // 3. Créer l'entité
        const user = User.create({
            email:    input.email,
            password: hashedPassword,
            name:     input.name,
        });

        // 4. Persister
        await this.userRepo.save(user);

        // 5. Envoyer email de bienvenue (optionnel — ne pas faire échouer si ça rate)
        this.emailSvc.sendWelcome(user.email).catch(console.error);

        // 6. Retourner le DTO (jamais l'entité complète — sécurité)
        return { id: user.id, name: user.name, email: user.email };
    }

    async changePassword(userId: string, newPassword: string): Promise<void> {
        const user = await this.userRepo.findById(userId);
        if (!user) throw new NotFoundError("Utilisateur introuvable");

        const hashed = await this.hashSvc.hash(newPassword);
        user.changePassword(hashed);   // Méthode de l'entité

        await this.userRepo.save(user);
        this.emailSvc.sendPasswordChanged(user.email).catch(console.error);
    }
}
```

<br>

---

## 3. Factory Pattern

```typescript title="TypeScript — Factory Pattern : centraliser la création d'objets complexes"
// ─── Simple Factory Function ──────────────────────────────────────────────────
function createNotification(type: "email" | "sms" | "push", data: NotifData): Notification {
    switch (type) {
        case "email": return new EmailNotification(data);
        case "sms":   return new SmsNotification(data);
        case "push":  return new PushNotification(data);
        default:
            const _exhaustive: never = type;
            throw new Error(`Type de notification inconnu : ${_exhaustive}`);
    }
}

// ─── Abstract Factory ─────────────────────────────────────────────────────────
interface StorageFactory {
    createUserRepository():    UserRepository;
    createArticleRepository(): ArticleRepository;
}

class SqlStorageFactory implements StorageFactory {
    constructor(private prisma: PrismaClient) {}
    createUserRepository()    { return new PrismaUserRepository(this.prisma); }
    createArticleRepository() { return new PrismaArticleRepository(this.prisma); }
}

class InMemoryStorageFactory implements StorageFactory {
    createUserRepository()    { return new InMemoryUserRepository(); }
    createArticleRepository() { return new InMemoryArticleRepository(); }
}

// En production :
const factory = new SqlStorageFactory(new PrismaClient());
// En tests :
const factory = new InMemoryStorageFactory();

const userRepo    = factory.createUserRepository();
const articleRepo = factory.createArticleRepository();
```

<br>

---

## 4. Observer / Event Pattern

```typescript title="TypeScript — Observer Pattern : découpler les réacteurs"
// ─── Event Bus simple ────────────────────────────────────────────────────────
type EventHandler<T> = (event: T) => Promise<void> | void;

class EventBus {
    private readonly handlers = new Map<string, EventHandler<unknown>[]>();

    subscribe<T>(event: string, handler: EventHandler<T>): void {
        const existing = this.handlers.get(event) ?? [];
        this.handlers.set(event, [...existing, handler as EventHandler<unknown>]);
    }

    async publish<T>(event: string, data: T): Promise<void> {
        const handlers = this.handlers.get(event) ?? [];
        await Promise.allSettled(handlers.map(handler => handler(data)));
    }
}

// ─── Définir les événements (typage fort) ────────────────────────────────────
interface UserRegisteredEvent {
    userId:    string;
    email:     string;
    name:      string;
    timestamp: Date;
}

interface ArticlePublishedEvent {
    articleId: string;
    authorId:  string;
    title:     string;
}

// ─── Utilisation dans un use case ────────────────────────────────────────────
class RegisterUserUseCase {
    constructor(
        private userRepo: UserRepository,
        private eventBus: EventBus,
    ) {}

    async execute(input: RegisterInput): Promise<void> {
        const user = User.create(input);
        await this.userRepo.save(user);

        // Publier l'événement — tous les abonnés seront notifiés
        await this.eventBus.publish<UserRegisteredEvent>('user.registered', {
            userId:    user.id,
            email:     user.email,
            name:      user.name,
            timestamp: new Date(),
        });
    }
}

// ─── Handlers (abonnés) ──────────────────────────────────────────────────────
const eventBus = new EventBus();

// Envoyer un email de bienvenue
eventBus.subscribe<UserRegisteredEvent>('user.registered', async (event) => {
    await emailService.sendWelcome(event.email, event.name);
});

// Logger l'inscription
eventBus.subscribe<UserRegisteredEvent>('user.registered', (event) => {
    logger.info(`Nouvel utilisateur : ${event.email} (${event.userId})`);
});

// Créer les préférences par défaut
eventBus.subscribe<UserRegisteredEvent>('user.registered', async (event) => {
    await preferencesService.createDefaults(event.userId);
});
```

<br>

---

## 5. CQRS — Command Query Responsibility Segregation

```typescript title="TypeScript — CQRS : séparer lectures et écritures"
// ─── COMMANDS (modifications d'état) ─────────────────────────────────────────
interface Command { readonly type: string; }

interface CreateArticleCommand extends Command {
    readonly type:     "CREATE_ARTICLE";
    readonly title:    string;
    readonly content:  string;
    readonly authorId: string;
}

interface PublishArticleCommand extends Command {
    readonly type:       "PUBLISH_ARTICLE";
    readonly articleId:  string;
    readonly publisherId: string;
}

// ─── QUERIES (lectures sans effet de bord) ────────────────────────────────────
interface Query { readonly type: string; }

interface GetArticleQuery extends Query {
    readonly type:      "GET_ARTICLE";
    readonly articleId: string;
}

interface SearchArticlesQuery extends Query {
    readonly type:    "SEARCH_ARTICLES";
    readonly term:    string;
    readonly status?: "draft" | "published";
    readonly page:    number;
}

// ─── Handlers ─────────────────────────────────────────────────────────────────
class CreateArticleHandler {
    constructor(private articleRepo: ArticleRepository, private eventBus: EventBus) {}

    async handle(cmd: CreateArticleCommand): Promise<string> {
        const article = Article.create({
            title:    cmd.title,
            content:  cmd.content,
            authorId: cmd.authorId,
        });
        await this.articleRepo.save(article);
        await this.eventBus.publish('article.created', { articleId: article.id });
        return article.id;
    }
}

class SearchArticlesHandler {
    constructor(private readRepo: ArticleReadRepository) {}  // Repository de lecture séparé

    async handle(query: SearchArticlesQuery): Promise<ArticleListDTO[]> {
        // La lecture peut utiliser un modèle optimisé (vue SQL, Elasticsearch...)
        return this.readRepo.search(query.term, query.status, query.page);
    }
}

// ─── Command/Query Bus ────────────────────────────────────────────────────────
class CommandBus {
    private handlers = new Map();

    register<T extends Command>(type: string, handler: { handle(cmd: T): Promise<unknown> }) {
        this.handlers.set(type, handler);
    }

    async dispatch<T extends Command>(command: T): Promise<unknown> {
        const handler = this.handlers.get(command.type);
        if (!handler) throw new Error(`No handler for ${command.type}`);
        return handler.handle(command);
    }
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le **Repository** abstrait la persistance derrière une interface — swap MySQL ↔ MongoDB sans toucher au domaine. Le **Service Layer** orchestre plusieurs repositories et opérations dans un cas d'usage cohérent. La **Factory** centralise la création d'objets complexes ou polymorphes. L'**Observer/Event Bus** découple les effets secondaires (email, logs, notifications) du flux principal. **CQRS** sépare les modèles de lecture et d'écriture pour optimiser chacun indépendamment. Ces patterns ne sont pas des dogmes — appliquez-les progressivement, quand la complexité le justifie.

> **Formation Architecture complète.** Retour à l'[index →](./index.md).

<br>
