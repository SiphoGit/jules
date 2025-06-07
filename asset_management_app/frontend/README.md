# Frontend - AI Asset Management UI

This directory contains the Next.js, React, and TypeScript frontend for the AI Asset Management application.

## Features

- **User Interface**: Clean UI components styled with TailwindCSS.
- **Pages**:
    - Login Page (mock authentication)
    - Dashboard Page (client overview)
    - Client Portfolio Page (detailed asset view)
    - Asset Recommendations Page (AI-driven suggestions)
- **API Integration**: Service layer for communicating with the backend FastAPI.

## Technology Stack

- Next.js: React framework for server-side rendering, static site generation, etc.
- React: JavaScript library for building user interfaces.
- TypeScript: Typed superset of JavaScript.
- TailwindCSS: Utility-first CSS framework for rapid UI development.
- ESLint: Pluggable linting utility for JavaScript and JSX.

## Setup and Running

1.  **Navigate to this directory**:
    ```bash
    cd path/to/asset_management_app/frontend
    ```

2.  **Install dependencies**:
    It's recommended to use Node.js version 18.x or later.
    ```bash
    npm install
    # or
    # yarn install
    ```
    This will install Next.js, React, TailwindCSS, and other necessary packages defined in `package.json`.

3.  **Environment Variables**:
    The application uses an environment variable to define the backend API's base URL. Create a `.env.local` file in this (`frontend`) directory:
    ```env
    NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
    ```
    Adjust the URL if your backend runs on a different host or port.

4.  **Run the development server**:
    ```bash
    npm run dev
    # or
    # yarn dev
    ```
    This will start the Next.js development server, usually on `http://localhost:3000`.

5.  **Open the application**:
    Open [http://localhost:3000](http://localhost:3000) in your browser to view the application.

## Project Structure (using `src` directory and App Router)

- `src/app/`: Contains page components and layouts for the App Router.
    - `layout.tsx`: Root layout for the application.
    - `page.tsx`: Homepage component.
    - `globals.css`: Global styles and TailwindCSS imports.
    - `login/page.tsx`: Login page component.
    - `dashboard/page.tsx`: Dashboard page component.
    - `clients/[clientId]/portfolio/page.tsx`: Dynamic page for client portfolio.
    - `clients/[clientId]/recommendations/page.tsx`: Dynamic page for asset recommendations.
- `src/components/`: Reusable React components (e.g., `Navbar.tsx`, `Layout.tsx`, `ClientCard.tsx`, `AssetTable.tsx`).
- `src/services/`: Modules for external interactions, like `api.ts` for backend communication.
- `public/`: Static assets.
- `tailwind.config.ts`: TailwindCSS configuration file.
- `next.config.js` (or `.mjs`): Next.js configuration file.
- `tsconfig.json`: TypeScript configuration.
- `package.json`: Project dependencies and scripts.

## Building for Production

To create a production build:
```bash
npm run build
# or
# yarn build
```
This will generate an optimized build in the `.next` directory. To run the production server:
```bash
npm start
# or
# yarn start
```
Note: Build issues were encountered in the automated subtask environment due to `node_modules/.bin` problems. This step should work in a standard local development environment.
