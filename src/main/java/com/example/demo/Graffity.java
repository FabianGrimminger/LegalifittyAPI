package com.example.demo;


import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import javax.persistence.*;
import java.io.File;
import java.nio.file.Paths;
import java.util.UUID;

@Entity
@EntityListeners(AuditingEntityListener.class)
public class Graffity {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    private UUID uuid;

    private User owner;

    public UUID getUuid() {
        return uuid;
    }

    public void setUuid(UUID uuid) {
        this.uuid = uuid;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public User getOwner() {
        return owner;
    }

    public void setOwner(User owner) {
        this.owner = owner;
    }

    /*public String buildDownloadPath(){
        File uploadDirectory = new File("new folder");
        if(!uploadDirectory.exists()){
            uploadDirectory.mkdir();
        }
        return Paths.get(System.getProperty("user.home").toString(), this.getUuid().toString() + ".png").toString();
    }*/
}
