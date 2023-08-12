import React from "react";
import styles from './sources.module.css'
import Image from 'next/image'
import Link from 'next/link'

const MAX_NUMBER_OF_CHARACTERS = 300;

export class Sources extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    formatTime(seconds) {
        let hours = Math.floor(seconds / 3600);
        let minutes = Math.floor((seconds % 3600) / 60);
        let remainingSeconds = seconds % 60;

        // Add leading zeros if needed
        if (hours < 10) {
            hours = "0" + hours;
        }
        if (minutes < 10) {
            minutes = "0" + minutes;
        }
        if (remainingSeconds < 10) {
            remainingSeconds = "0" + remainingSeconds;
        }

        return hours + ":" + minutes + ":" + remainingSeconds;
    }

    render() {
        const { text, link, title, time } = this.props;

        var thumbnail = "";

        var titleStyles = styles.title;

        if (link.split("v=").length > 1) {
            if (link.split("v=")[1].split("&").length > 1) {
                const videoId = link.split("v=")[1].split("&")[0];
                thumbnail = `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`
                titleStyles = styles.titleWithThumbnail;
            }
        }

        return (
            <div className={styles.episodeSection}>
                <div className={styles.content}>
                    {thumbnail !== "" ? (
                        <div className={styles.topSection}>
                            <div className={styles.thumbnail}>
                                <a href={link} target="_blank">
                                    <Image
                                        src={thumbnail}
                                        alt={`YouTube ${title}`}
                                        width={110}
                                        height={70}
                                        unoptimized
                                    />
                                </a>
                            </div>
                            <div className={titleStyles}>
                                <a className={styles.link} href={link} target="_blank">{title} @ {this.formatTime(time)}</a>
                            </div>
                        </div>
                    ) : (
                        <div className={titleStyles}>
                            <a className={styles.link} href={link} target="_blank">{title} @ {this.formatTime(time)}</a>
                        </div>
                    )}

                    <p>{text.slice(0, MAX_NUMBER_OF_CHARACTERS)}</p>
                </div>
            </div>
        );
    }
}