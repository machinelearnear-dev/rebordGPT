import React from 'react';
import styles from './header.module.css'
import Image from "next/image";
import Link from 'next/link';

export class Header extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className={styles.header}>
                <div className={styles.logo}>
                    <Link href="/">
                        <Image
                            src="/logo.jpg"
                            alt="Rebord GPT"
                            height={40}
                            width={40}
                        />
                    </Link>
                </div >
                <div>
                    <Link href="/" className={styles.titleText}>
                        <h3 className={styles.title}>RebordGPT</h3>
                    </Link>
                </div>
            </div>
        );
    }
}

