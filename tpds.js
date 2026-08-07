'use strict';

/**
 * Copyright 2022 Adobe. A
ll rights reserved.
 * This file is licensed 
to you under the Apache License, Version 2.0 
(the "License");
 * you may not use this file
 except in compliance with the License. You m
ay obtain a copy
 * of the License at http://
www.apache.org/licenses/LICENSE-2.0
 *
 * Unl
ess required by applicable law or agreed to i
n writing, software distributed under
 * the 
License is distributed on an "AS IS" BASIS, W
ITHOUT WARRANTIES OR REPRESENTATIONS
 * OF AN
Y KIND, either express or implied. See the Li
cense for the specific language
 * governing 
permissions and limitations under the License
.
 */

const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const tpdSch
ema = new Schema({
    total: Number,
    tld
: String,
    zones: [{
        zone: String,

        records: [{
            host: String
,
            target: String,
        }],
   
 }],
}, {
    collection: 'tpds',
});

const 
tpdModel = mongoose.model('tpdModel', tpdSche
ma);

module.exports = {
    TPDModel: tpdMod
el,
    getTPDsByZone: function (zone, listOn
ly) {
        let promise;
        if (!listO
nly) {
            promise = tpdModel.find({ 
'zones.zone': zone }).exec();
        } else 
{
            promise = tpdModel.find({
     
           'zones.zone': zone,
            },
 { 'tld': 1, 'zones.zone': 1 }).exec();
     
   }
        return (promise);
    },
    get
TPDsByTPD: function (tpd) {
        return tp
dModel.findOne({ 'tld': tpd });
    },
    ge
tTPDsByWildcard: function (search, listOnly) 
{
        let promise;
        let AWSregex =
 new RegExp('.*' + search + '$');
        if 
(listOnly) {
            promise = tpdModel.f
ind({
                'tld': { '$regex': AWSr
egex },
            }, { 'tld': 1, 'zones.zon
e': 1 }).exec();
        } else {
           
 promise = tpdModel.find({ 'tld': { '$regex':
 AWSregex } }).exec();
        }
        retu
rn (promise);
    },
    getAllTPDs: function
 () {
        return tpdModel.find({}).sort({
 'total': -1 }).exec();
    },
};


