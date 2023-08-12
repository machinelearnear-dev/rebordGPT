import React from 'react';
import styles from './layout.module.css'
import { Header } from '../header/header';
import Head from 'next/head';

export class Layout extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        const { children } = this.props;
        return (
            <>
                <Head>
                    <title>Rebord GPT</title>
                    <meta name="description" content="Rebord GPT" />
                    <meta name="viewport" content="width=device-width, initial-scale=1" />
                    <link rel="icon" href="/logo.jpg" />
                </Head>
                <div className={styles.container}>
                    <Header />
                    <div className={styles.main}>
                        <main>
                            {children}
                        </main>
                    </div>
                </div>
            </>
        );
    }
}

