import asyncio
import logging
from multiprocessing import Process
from time import sleep

import git

from metadata import root_dir
from salt_client import SaltClient
from sound_handler import normalize_audio_clips


def bot_wrapper(token: str):
    normalize_audio_clips()

    client = SaltClient()

    loop = asyncio.get_event_loop()
    loop.create_task(client.start(token))
    p = Process(target=loop.run_forever)
    p.start()

    repo = git.Repo(root_dir())

    try:
        while True:
            # Check once a minute
            sleep(60)

            # Check for new commits on origin
            branch = repo.active_branch
            repo.remotes.origin.fetch()
            n_new = len(list(repo.iter_commits(f"{branch}..origin/{branch}")))

            # If new commits detected
            if n_new > 0:
                logging.info(f"Pulling from {branch}")
                repo.remotes.origin.pull()

                # Renormalize audio
                normalize_audio_clips()

                # Restart client
                task = loop.create_task(client.close())
                while not task.done():
                    pass

                loop.create_task(client.start(token))
    except (KeyboardInterrupt, InterruptedError):
        p.terminate()
