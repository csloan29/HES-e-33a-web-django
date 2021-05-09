document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', () => compose_email(null, null));
    document.querySelector('#compose-send-btn').addEventListener('click', () => send_email());

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email(email, fromSent) {

    // Show compose view and hide other views
    document.querySelector('#mailbox-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    recipients = document.querySelector('#compose-recipients');
    subject = document.querySelector('#compose-subject');
    body = document.querySelector('#compose-body');

    // Clear out composition fields
    recipients.value = '';
    subject.value = '';
    body.value = '';

    // if replying to email, prefill inputs
    if (email != null) {
        // if composing email reply coming from a sent email
        // (as in you are adding another email to the chain)
        // be sure to flip the sender and subject as the
        // data does not indicate it is a sent or received email
        if (fromSent) {
            recipients.value += email.recipients;
        } else {
            recipients.value += email.sender;
        }
        if (email.subject.substring(0, 3) == 'Re:') {
            subject.value = email.subject;
        } else {
            subject.value = "Re: " + email.subject;
        }
        body.value += "\n\nOn " + email.timestamp + " " + email.sender + " wrote:\n" + email.body;
    }
}

function load_mailbox(mailbox) {
    // Show the mailbox name (this also acts as a way to clear out old data)
    const title = document.querySelector('#mailbox-view');
    title.innerHTML = `<h3 class="mb-3">${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`; //todo: 2.3: already done

    // fetch all emails for provided mailbox
    fetch('/emails/' + mailbox)
    .then(response => response.json())
    .then(emails => {
        // create bootstrap row and column container for email cards
        const row = document.createElement('div');
        row.classList.add('row');
        const column = document.createElement('div');
        column.classList.add('col');

        // create card for each email and add to inbox column
        emails.forEach(email => {
            // create all necessary elements for email card
            const card = document.createElement('div');
            const cardBody = document.createElement('div');
            const cardBodyRow = document.createElement('div');
            const cardBodyColSender = document.createElement('div');
            const cardBodyColSubject = document.createElement('div');
            const cardBodyColTimeStamp = document.createElement('div');
            const cardBodyColBtn = document.createElement('div');
            const cardTitle = document.createElement('h5');

            // add all data to email row
            if (mailbox == 'sent') {
                cardBodyColSender.innerHTML = 'To: ' + email.recipients;
            } else {
                cardBodyColSender.innerHTML = email.sender;
            }
            cardTitle.innerText = email.subject;
            cardBodyColSubject.innerHTML = email.subject;
            cardBodyColTimeStamp.innerHTML = email.timestamp;

            // add all necessary classes to elements
            card.classList.add('card');
            card.classList.add('mt-1');
            cardBody.classList.add('card-body');
            cardBodyRow.classList.add('row');
            cardBodyRow.classList.add('align-items-center');
            cardBodyColSender.classList.add('col-3');
            cardBodyColSubject.classList.add('col-5');
            cardBodyColTimeStamp.classList.add('col-3');
            cardBodyColBtn.classList.add('col-1');
            email.read ? card.classList.add('bg-light') : card.classList.add('bg-white');

            //add event listeners to all necessary elements
            card.addEventListener('click', () => load_email(email.id, mailbox));

            //create archive button for inbox and archived email
            if (mailbox != 'sent') {
                //create button elements
                const archiveBtn = document.createElement('button');
                const btnIcon = document.createElement('i');

                //add necessary classes for archive buttons
                archiveBtn.classList.add('btn');
                btnIcon.classList.add('fa');
                if (email.archived) {
                    btnIcon.classList.add('fa-undo');
                    archiveBtn.classList.add('btn-success');
                    //archive email button listener
                    archiveBtn.addEventListener('click', function(event) {
                        event.stopPropagation();
                        archive_email(email.id, false)
                    });
                } else {
                    btnIcon.classList.add('fa-archive');
                    archiveBtn.classList.add('btn-secondary');
                    //archive email button listener
                    archiveBtn.addEventListener('click', function(event) {
                        event.stopPropagation();
                        archive_email(email.id, true)
                    });
                }

                //add to DOM
                archiveBtn.append(btnIcon);
                cardBodyColBtn.append(archiveBtn);
            }

            //insert all elements to DOM tree
            cardBodyRow.append(cardBodyColSender);
            cardBodyRow.append(cardBodyColSubject);
            cardBodyRow.append(cardBodyColTimeStamp);
            cardBodyRow.append(cardBodyColBtn);
            cardBody.append(cardBodyRow);
            card.append(cardBody);
            column.append(card);
        });

        //add final card list to DOM
        row.append(column);
        document.querySelector('#mailbox-view').append(row);
    });

    // Show the mailbox and hide other views
    document.querySelector('#mailbox-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
}

function send_email() {
    sender = document.getElementById('compose-sender').value;
    recipients = document.getElementById('compose-recipients').value;
    subject = document.getElementById('compose-subject').value;
    body = document.getElementById('compose-body').value;
    //todo: validation ?
    email = {
        'sender': sender,
        'recipients': recipients,
        'subject': subject,
        'body': body,
    }

    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify(email)
    })
    .then(() => {
        load_mailbox('sent');
    });
}

function load_email(id, mailbox) {
    //fetch all necessary elements for data insertion
    const title = document.querySelector('#email-subject');
    const timestamp = document.querySelector('#email-timestamp');
    const sender = document.querySelector('#email-sender');
    const recipients = document.querySelector('#recipients');
    const body = document.querySelector('#email-body');
    const replyBtn = document.querySelector('#reply-btn');

    //first clear values in view
    title.innerHTML = '';
    timestamp.innerHTML = '';
    sender.innerHTML = '';
    recipients.innerHTML = '';
    body.innerHTML = '';

    fetch('/emails/' + id)
    .then(response => response.json())
    .then(email => {
        //first, mark email as read; waiting for response unnecessary
        fetch('/emails/' + id, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
        })

        //add all necessary email data to elements
        title.innerText = email.subject;
        timestamp.innerText = email.timestamp;
        sender.innerText = "From: " + email.sender;
        recipients.append("To: ");
        email.recipients.forEach((r, idx, array) => {
            if (idx === array.length - 1) {
                var recipientTextNode = document.createTextNode(r);
            } else {
                var recipientTextNode = document.createTextNode(r + ',');
            }
            recipients.appendChild(recipientTextNode);
        });
        body.innerText = email.body;

        //add reply button click listener
        replyBtn.addEventListener('click', () => {
            compose_email(email, mailbox == 'sent');
        });

        // Show the email view and hide other views
        document.querySelector('#email-view').style.display = 'block';
        document.querySelector('#mailbox-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
    });
}

function archive_email(id, markArchived) {
    fetch('/emails/' + id, {
        method: 'PUT',
        body: JSON.stringify({
            archived: markArchived
        })
    })
    .then(() => {
        load_mailbox('inbox');
    });
}
