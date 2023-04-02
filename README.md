# Vage

The Vage is a AI virtual canvas desktop application built using `Electron` and a variety of open-source tools and frameworks. The application leverages Google's `Mediapipe` framework for hand tracking, enabling users to draw and create designs using their hands. In the backend, the application uses `OpenCV` with Python to provide computer vision capabilities, enabling the application to recognize and interpret hand movements accurately.

## Screenshots

![App Screenshot](https://github.com/ashutosh-s15/GIFs/blob/main/vage-demo.jpg)

## Usage

### Python

Install dependencies:

```bash
pip install opencv-python mediapipe
```

### Electron

Install dependencies:

```bash
npm install
```

Run:

```bash
npm start
```

You can also use `Electronmon` to constantly run and not have to reload after making changes

```bash
npx electronmon .
```

## Packaging

There are multiple ways to package Electron apps. Vage is packaged using [Electron Packager](https://www.npmjs.com/package/electron-packager) into OS-specific bundles.

## Developer Mode

If your `NODE_ENV` is set to `development` then you will have the dev tools enabled and available in the menu bar. It will also open them by default.

When set to `production`, the dev tools will not be available.

## Authors

- [@AshutoshSingh](https://www.github.com/ashutosh-s15)
